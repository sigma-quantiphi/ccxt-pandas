"""Open orders data schema."""

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class OpenOrdersSchema(BaseExchangeSchema):
    """Open orders data schema.

    Used by methods like fetch_open_orders, fetch_open_order.

    Returns currently open (unfilled or partially filled) orders.
    This serves as the base schema for order fetching operations.
    """

    # Required fields
    id: Series[str] = pa.Field(
        title="Order ID", description="Unique order identifier"
    )
    timestamp: Series[pd.Timestamp] = pa.Field(
        title="Timestamp", description="Order creation timestamp"
    )
    datetime: Series[pd.Timestamp] = pa.Field(
        title="Datetime", description="Order creation datetime (alias)"
    )
    lastUpdateTimestamp: Series[pd.Timestamp] = pa.Field(
        title="Last Update Timestamp", description="Last order update timestamp"
    )
    symbol: Series[str] = pa.Field(
        title="Symbol", description="Trading pair"
    )
    type: Series[str] = pa.Field(
        title="Type", description="Order type (e.g., limit, market)"
    )
    side: Series[str] = pa.Field(
        isin=["buy", "sell"], title="Side", description="Order side: 'buy' or 'sell'"
    )
    price: Series[float] = pa.Field(
        ge=0, title="Price", description="Order price"
    )
    cost: Series[float] = pa.Field(
        ge=0, title="Cost", description="Total cost (filled amount * price)"
    )
    amount: Series[float] = pa.Field(
        ge=0, title="Amount", description="Order amount"
    )
    filled: Series[float] = pa.Field(
        ge=0, title="Filled", description="Filled amount"
    )
    remaining: Series[float] = pa.Field(
        ge=0, title="Remaining", description="Remaining amount to be filled"
    )
    status: Series[str] = pa.Field(
        title="Status", description="Order status (e.g., open, closed, canceled)"
    )
    trades: Series[object] = pa.Field(
        title="Trades", description="List of trades that filled this order"
    )
    reduceOnly: Series[bool] = pa.Field(
        title="Reduce Only", description="Whether order is reduce-only (derivatives)"
    )
    fees: Series[object] = pa.Field(
        title="Fees", description="Fee details (list of dicts)"
    )
    fee_cost: Series[float] = pa.Field(
        ge=0, title="Fee Cost", description="Total fee amount"
    )
    fee_currency: Series[str] = pa.Field(
        title="Fee Currency", description="Currency in which fee was charged"
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
