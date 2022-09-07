"""Stream type classes for tap-leaflink."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_leaflink.client import leaflinkStream

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.


class CustomersStream(leaflinkStream):
    """Customers Stream"""

    name = "customers"
    path = "/customers/"
    primary_keys = ["id"]
    # replication_key = "modified"
    # replication_method = "INCREMENTAL"
    schema_filepath = SCHEMAS_DIR / "customers.json"


class ProductsStream(leaflinkStream):
    """Products Stream"""

    name = "products"
    path = "/products/"
    primary_keys = ["id"]
    schema_filepath = SCHEMAS_DIR / "products.json"


class OrderEventLogsStream(leaflinkStream):
    """Order Event Logs Stream"""

    name = "order_event_logs"
    path = "/order-event-logs/"
    primary_keys = ["id"]
    # replication_key = "modified"
    # replication_method = "INCREMENTAL"
    schema_filepath = SCHEMAS_DIR / "order-event-logs.json"


class OrdersReceivedStream(leaflinkStream):
    """Orders Received Stream"""

    name = "orders_received"
    path = "/orders-received/"
    primary_keys = ["number"]
    # replication_key = "modified"
    # replication_method = "INCREMENTAL"
    schema_filepath = SCHEMAS_DIR / "orders-received.json"

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "order_number": record["number"]
        }


class LineItemsStream(leaflinkStream):
    """Line Items Stream"""

    parent_stream_type = OrdersReceivedStream

    name = "line_items"
    primary_keys = ["id"]
    # replication_key = None
    path = "/orders-received/{order_number}/line-items/"
    schema_filepath = SCHEMAS_DIR / "line-items.json"


class ProductCategoriesStream(leaflinkStream):
    """Product Categories Stream"""

    name = "product_categories"
    path = "/product-categories/"
    primary_keys = ["id"]
    schema_filepath = SCHEMAS_DIR / "product-categories.json"


class ProductLinesStream(leaflinkStream):
    """Product Lines Stream"""

    name = "product_lines"
    path = "/product-lines/"
    primary_keys = ["id"]
    schema_filepath = SCHEMAS_DIR / "product-lines.json"
