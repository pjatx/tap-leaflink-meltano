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
    """Define custom stream."""
    name = "customers"
    path = "/customers/"
    primary_keys = ["id"]
    replication_key = "modified"
    replication_method = "INCREMENTAL"
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    schema_filepath = SCHEMAS_DIR / "customers.json"

class ProductsStream(leaflinkStream):
    """Define custom stream."""
    name = "products"
    path = "/products/"
    primary_keys = ["id"]
    replication_key = None
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    schema_filepath = SCHEMAS_DIR / "products.json"

class LineItemsStream(leaflinkStream):
    """Define custom stream."""
    name = "line-items"
    path = "/line-items/"
    primary_keys = ["id"]
    replication_key = None
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    schema_filepath = SCHEMAS_DIR / "line-items.json"

class OrderEventLogsStream(leaflinkStream):
    """Define custom stream."""
    name = "order-event-logs"
    path = "/order-event-logs/"
    primary_keys = ["id"]
    replication_key = None
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    schema_filepath = SCHEMAS_DIR / "order-event-logs.json"

class OrdersReceivedStream(leaflinkStream):
    """Define custom stream."""
    name = "orders-received"
    path = "/orders-received/"
    primary_keys = ["number"]
    replication_key = None
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    schema_filepath = SCHEMAS_DIR / "orders-received.json"

class ProductCategoriesStream(leaflinkStream):
    """Define custom stream."""
    name = "product-categories"
    path = "/product-categories/"
    primary_keys = ["id"]
    replication_key = None
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    schema_filepath = SCHEMAS_DIR / "product-categories.json"

class ProductLinesStream(leaflinkStream):
    """Define custom stream."""
    name = "product-lines"
    path = "/product-lines/"
    primary_keys = ["id"]
    replication_key = None
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    schema_filepath = SCHEMAS_DIR / "product-lines.json"