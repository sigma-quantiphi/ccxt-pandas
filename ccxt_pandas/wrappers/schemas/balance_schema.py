"""Balance and wallet data schema."""

from typing import Optional

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class BalanceSchema(BaseExchangeSchema):
    """Balance/wallet data schema.

    Used by methods like fetch_balance, watch_balance.

    Supports both regular balances (with 'code' field) and margin balances
    (with 'symbol' field and base_/quote_ prefixed columns).
    """

    # Regular balance fields (for spot/wallet balances)
    code: Optional[Series[str]] = pa.Field(
        nullable=True, title="Code", description="Currency code (spot balances)"
    )
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

    # Margin balance fields (for margin/cross balances)
    symbol: Optional[Series[str]] = pa.Field(
        nullable=True, title="Symbol", description="Trading pair (margin balances)"
    )
    base_free: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Base Free", description="Available base currency"
    )
    base_used: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Base Used", description="Base currency in open orders"
    )
    base_total: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Base Total", description="Total base currency"
    )
    base_debt: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Base Debt", description="Borrowed base currency"
    )
    quote_free: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Quote Free", description="Available quote currency"
    )
    quote_used: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Quote Used", description="Quote currency in open orders"
    )
    quote_total: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Quote Total", description="Total quote currency"
    )
    quote_debt: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Quote Debt", description="Borrowed quote currency"
    )

    # These fields appear in some exchange formats
    base: Optional[Series[str]] = pa.Field(
        nullable=True, title="Base", description="Base currency identifier"
    )
    quote: Optional[Series[str]] = pa.Field(
        nullable=True,
        title="Quote",
        description="Quote currency identifier",
    )
    timestamp: Optional[Series[pd.Timestamp]] = pa.Field(
        nullable=True, title="Timestamp", description="Balance snapshot timestamp"
    )
    datetime: Optional[Series[pd.Timestamp]] = pa.Field(
        nullable=True, title="Datetime", description="Balance snapshot datetime (alias)"
    )
