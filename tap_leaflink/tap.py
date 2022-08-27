"""leaflink tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  
from tap_leaflink.streams import (
    CustomersStream,
    LineItemsStream,
    OrderEventLogsStream,
    OrdersReceivedStream,
    ProductCategoriesStream,
    ProductLinesStream,
    ProductsStream,
)

STREAM_TYPES = [
    CustomersStream,
    LineItemsStream,
    OrderEventLogsStream,
    OrdersReceivedStream,
    ProductCategoriesStream,
    ProductLinesStream,
    ProductsStream,
]


class Tapleaflink(Tap):
    """leaflink tap class."""
    name = "tap-leaflink"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
            required=True,
            description="The token to authenticate against the API service"
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync"
        ),
        th.Property(
            "api_url",
            th.StringType,
            default="https://www.leaflink.com/api/v2",
            description="The url for the API service"
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
