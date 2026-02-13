"""Trade data schemas for public and user trades."""

from typing import Optional

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema, FeeFieldsMixin


class TradeSchema(BaseExchangeSchema):
    """Public trade data schema.

    Used by methods like fetch_trades.

    These are public market trades visible to all users.
    Most fields are required except fees and exchange.
    """

    # Timestamps (required)
    timestamp: Series[pd.Timestamp] = pa.Field(
        title="Timestamp", description="Trade timestamp"
    )
    datetime: Series[pd.Timestamp] = pa.Field(
        title="Datetime", description="Trade datetime (alias)"
    )

    # Core trade fields (all required)
    symbol: Series[str] = pa.Field(
        title="Symbol", description="Trading pair"
    )
    id: Series[str] = pa.Field(
        unique=True, title="Trade ID", description="Unique trade identifier"
    )
    side: Series[str] = pa.Field(
        isin=["buy", "sell"], title="Side", description="Trade side: 'buy' or 'sell'"
    )
    price: Series[float] = pa.Field(
        ge=0, title="Price", description="Trade price"
    )
    amount: Series[float] = pa.Field(
        ge=0, title="Amount", description="Trade amount"
    )
    cost: Series[float] = pa.Field(
        ge=0, title="Cost", description="Trade cost (price * amount)"
    )

    # Optional fields
    fees: Optional[Series[object]] = pa.Field(
        nullable=True, title="Fees", description="Fee information (can be dict or list)"
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)


class MyTradesSchema(TradeSchema, FeeFieldsMixin):
    """User trades (my trades) data schema.

    Used by methods like fetch_my_trades, fetch_order_trades.

    Returns the authenticated user's trade history including fees and order references.
    Inherits all fields from TradeSchema and FeeFieldsMixin, and adds:
    - order (order ID that generated the trade)
    - takerOrMaker (whether trade was taker or maker)

    The fees field and fee fields are required (overriding the optional in parent classes).
    """

    # Additional required fields for user trades
    order: Series[str] = pa.Field(
        title="Order ID", description="Order ID that generated this trade"
    )
    takerOrMaker: Series[str] = pa.Field(
        isin=["taker", "maker"], title="Taker or Maker", description="Whether trade was taker or maker"
    )

    # Override to make fees required for user trades
    fees: Series[object] = pa.Field(
        title="Fees", description="Fee details (dict or list)"
    )

    # Override fee fields to make them required for user trades
    fee_currency: Series[str] = pa.Field(
        title="Fee Currency", description="Currency in which fee was charged"
    )
    fee_cost: Series[float] = pa.Field(
        ge=0, title="Fee Cost", description="Fee amount charged"
    )
