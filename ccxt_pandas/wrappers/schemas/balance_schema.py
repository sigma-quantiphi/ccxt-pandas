"""Balance and wallet data schema."""

from typing import Optional

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class BalanceSchema(BaseExchangeSchema):
    """Balance/wallet data schema.

    Used by methods like fetch_balance, watch_balance.

    Symbol is required (currency code). Balance amounts may be null
    depending on the exchange response format.
    """

    symbol: Series[str] = pa.Field(title="Symbol", description="Currency symbol/code")
    free: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Free", description="Available balance"
    )
    used: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Used", description="Balance in open orders"
    )
    total: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Total", description="Total balance (free + used)"
    )
    debt: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Debt", description="Borrowed amount (margin)"
    )

    # These fields appear in some exchange formats
    base: Optional[Series[str]] = pa.Field(
        nullable=True, title="Base", description="Base currency (when symbol is a pair)"
    )
    quote: Optional[Series[str]] = pa.Field(
        nullable=True,
        title="Quote",
        description="Quote currency (when symbol is a pair)",
    )
    timestamp: Optional[Series[pd.Timestamp]] = pa.Field(
        nullable=True, title="Timestamp", description="Balance snapshot timestamp"
    )
    datetime: Optional[Series[pd.Timestamp]] = pa.Field(
        nullable=True, title="Datetime", description="Balance snapshot datetime (alias)"
    )
