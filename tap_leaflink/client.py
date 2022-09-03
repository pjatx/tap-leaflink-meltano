"""REST client handling, including leaflinkStream base class."""
import logging
import requests
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from memoization import cached

from typing import Any, Callable, Dict, Generator, Iterable, List, Optional, Union, cast

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import APIKeyAuthenticator
from urllib import parse


def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))


logger = logging.getLogger(__name__)

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class leaflinkStream(RESTStream):
    """leaflink stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config["api_url"]

    records_jsonpath = "$.results[*]"  # Or override `parse_response`.
    next_page_token_jsonpath = "$.next"  # Or override `get_next_page_token`.

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Return a new authenticator object."""

        # Note, we're using a legacy API key here, so you'll want to change the value
        # of the Authorization key to match the new format in the docs:
        # https://developer.leaflink.com/api/docs/index.html#section/Authentication

        return APIKeyAuthenticator.create_for_stream(
            self,
            key="Authorization",
            value='App ' + self.config.get("api_key"),
            location="header"
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        # If not using an authenticator, you may also provide inline auth headers:
        # headers["Private-Token"] = self.config.get("auth_token")
        return headers

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""
        # TODO: If pagination is required, return a token which can be used to get the
        #       next page. If this is the final page, return "None" to end the
        #       pagination loop.
        if self.next_page_token_jsonpath:
            all_matches = extract_jsonpath(
                self.next_page_token_jsonpath, response.json()
            )
            first_match = next(iter(all_matches), None)
            next_page_token = first_match

            # if next_page_token:
            #     data = response.json()
            #     count = data['count']

            #     params = dict(parse.parse_qsl(parse.urlsplit(next_page_token).query))
            #     offset = int(params.get('offset', 0))
            #     print(str(round((offset / count) * 100, 2)) + "%")
            return next_page_token
        else:
            return None

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""

        params = {}

        # State management
        context_state = self.get_context_state(context)

        # prCyan(context_state)
        if context_state.get("progress_markers"):
            progress_markers = context_state.get("progress_markers")
            last_updated = progress_markers.get("replication_key_value")

            if last_updated:
                params["modified__gt"] = last_updated

        if next_page_token:

            parsed = parse.urlsplit(next_page_token)
            page = parsed.scheme + "://" + parsed.netloc + parsed.path

            params.update(dict(parse.parse_qsl(parse.urlsplit(next_page_token).query)))

        # prCyan(params)

        # start_date = self.config.get("start_date")
        # elif start_date:
        #     params["created_on__gt"] = start_date
        # logger.info(params)

        if len(params) > 0:
            return params
        else:
            return {}

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        # TODO: Parse response body and return a set of records.
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    def prepare_request(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> requests.PreparedRequest:
        """Prepare a request object.

        If partitioning is supported, the `context` object will contain the partition
        definitions. Pagination information can be parsed from `next_page_token` if
        `next_page_token` is not None.

        Args:
            context: Stream partition or context dictionary.
            next_page_token: Token, page number or any request argument to request the
                next page of data.

        Returns:
            Build a request with the stream's URL, path, query parameters,
            HTTP headers and authenticator.
        """
        http_method = self.rest_method
        url: str = self.get_url(context)
        params: dict = self.get_url_params(context, next_page_token)
        request_data = self.prepare_request_payload(context, next_page_token)
        headers = self.http_headers

        authenticator = self.authenticator
        if authenticator:
            headers.update(authenticator.auth_headers or {})
            params.update(authenticator.auth_params or {})

        request = cast(
            requests.PreparedRequest,
            self.requests_session.prepare_request(
                requests.Request(
                    method=http_method,
                    url=url,
                    params=params,
                    headers=headers,
                    json=request_data,
                ),
            ),
        )
        logger.info(request.url)
        return request
