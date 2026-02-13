"""Trade data schema for public trades."""

from typing import Optional

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


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
        title="Trade ID", description="Unique trade identifier"
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
