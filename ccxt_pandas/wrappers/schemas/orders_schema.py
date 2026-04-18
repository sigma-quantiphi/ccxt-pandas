"""Orders data schema."""

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema, FeeFieldsMixin


class OrdersSchema(BaseExchangeSchema, FeeFieldsMixin):
    """Orders data schema.

    Used by methods like fetch_open_orders, fetch_closed_orders, fetch_canceled_orders.

    Returns order information for both open and closed orders. Fields like
    clientOrderId, lastTradeTimestamp, timeInForce, and average are optional
    as they may not be present in open orders.
    """

    # Required fields
    id: Series[str] = pa.Field(title="Order ID", description="Unique order identifier")
    timestamp: Series[pd.Timestamp] = pa.Field(
        title="Timestamp", description="Order creation timestamp"
    )
    datetime: Series[pd.Timestamp] = pa.Field(
        title="Datetime", description="Order creation datetime (alias)"
    )
    lastUpdateTimestamp: Series[pd.Timestamp] = pa.Field(
        title="Last Update Timestamp", description="Last order update timestamp"
    )
    symbol: Series[str] = pa.Field(title="Symbol", description="Trading pair")
    type: Series[str] = pa.Field(title="Type", description="Order type (e.g., limit, market)")
    side: Series[str] = pa.Field(
        isin=["buy", "sell"], title="Side", description="Order side: 'buy' or 'sell'"
    )
    price: Series[float] = pa.Field(ge=0, title="Price", description="Order price")
    cost: Series[float] = pa.Field(
        ge=0, title="Cost", description="Total cost (filled amount * price)"
    )
    amount: Series[float] = pa.Field(ge=0, title="Amount", description="Order amount")
    filled: Series[float] = pa.Field(ge=0, title="Filled", description="Filled amount")
    remaining: Series[float] = pa.Field(
        ge=0, title="Remaining", description="Remaining amount to be filled"
    )
    status: Series[str] = pa.Field(
        title="Status", description="Order status (e.g., open, closed, canceled)"
    )
    trades: Series[object] = pa.Field(
        title="Trades", description="List of trades that filled this order"
    )
    fees: Series[object] = pa.Field(title="Fees", description="Fee details (list of dicts)")

    # Optional fields (vary by exchange and order state)
    clientOrderId: Series[str] | None = pa.Field(
        nullable=True,
        title="Client Order ID",
        description="User-defined order identifier",
    )
    lastTradeTimestamp: Series[pd.Timestamp] | None = pa.Field(
        nullable=True,
        title="Last Trade Timestamp",
        description="Timestamp of last trade execution",
    )
    timeInForce: Series[str] | None = pa.Field(
        nullable=True,
        title="Time In Force",
        description="Order time in force (e.g., GTC, IOC, FOK)",
    )
    average: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Average", description="Average fill price"
    )
    reduceOnly: Series[bool] | None = pa.Field(
        nullable=True,
        title="Reduce Only",
        description="Whether order is reduce-only (derivatives)",
    )
    postOnly: Series[bool] | None = pa.Field(
        nullable=True,
        title="Post Only",
        description="Whether order is post-only (maker-only)",
    )
    # Note: fee_currency, fee_cost, fee_rate come from FeeFieldsMixin (Optional)
    # Note: exchange field comes from BaseExchangeSchema (Optional)
