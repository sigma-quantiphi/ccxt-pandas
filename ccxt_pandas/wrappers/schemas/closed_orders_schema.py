"""Closed orders data schema."""

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.open_orders_schema import OpenOrdersSchema


class ClosedOrdersSchema(OpenOrdersSchema):
    """Closed orders data schema.

    Used by methods like fetch_closed_orders, fetch_canceled_orders.

    Returns closed (filled or canceled) orders with additional fields
    like client order ID, last trade timestamp, and average fill price.
    Inherits all fields from OpenOrdersSchema and adds:
    - clientOrderId
    - lastTradeTimestamp
    - timeInForce
    - average
    """

    # Additional fields for closed orders
    clientOrderId: Series[str] = pa.Field(
        title="Client Order ID", description="User-defined order identifier"
    )
    lastTradeTimestamp: Series[pd.Timestamp] = pa.Field(
        title="Last Trade Timestamp", description="Timestamp of last trade execution"
    )
    timeInForce: Series[str] = pa.Field(
        title="Time In Force", description="Order time in force (e.g., GTC, IOC, FOK)"
    )
    average: Series[float] = pa.Field(
        ge=0, title="Average", description="Average fill price"
    )
