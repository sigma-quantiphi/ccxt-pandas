"""User trades (my trades) data schema."""

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class MyTradesSchema(BaseExchangeSchema):
    """User trades (my trades) data schema.

    Used by methods like fetch_my_trades, fetch_order_trades.

    Returns the authenticated user's trade history including fees and order references.
    """

    # Required fields
    timestamp: Series[pd.Timestamp] = pa.Field(
        title="Timestamp", description="Trade execution timestamp"
    )
    datetime: Series[pd.Timestamp] = pa.Field(
        title="Datetime", description="Trade execution datetime (alias)"
    )
    symbol: Series[str] = pa.Field(
        title="Symbol", description="Trading pair"
    )
    id: Series[str] = pa.Field(
        title="Trade ID", description="Unique trade identifier"
    )
    order: Series[str] = pa.Field(
        title="Order ID", description="Order ID that generated this trade"
    )
    takerOrMaker: Series[str] = pa.Field(
        isin=["taker", "maker"], title="Taker or Maker", description="Whether trade was taker or maker"
    )
    side: Series[str] = pa.Field(
        isin=["buy", "sell"], title="Side", description="Trade side: 'buy' or 'sell'"
    )
    price: Series[float] = pa.Field(
        ge=0, title="Price", description="Trade execution price"
    )
    amount: Series[float] = pa.Field(
        ge=0, title="Amount", description="Trade amount in base currency"
    )
    cost: Series[float] = pa.Field(
        ge=0, title="Cost", description="Trade cost in quote currency (price * amount)"
    )
    fees: Series[object] = pa.Field(
        title="Fees", description="Fee details (dict or list)"
    )
    fee_currency: Series[str] = pa.Field(
        title="Fee Currency", description="Currency in which fee was charged"
    )
    fee_cost: Series[float] = pa.Field(
        ge=0, title="Fee Cost", description="Fee amount charged"
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
