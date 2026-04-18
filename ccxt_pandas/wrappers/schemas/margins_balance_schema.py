"""Margins balance data schema."""

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class MarginsBalanceSchema(BaseExchangeSchema):
    """Margins balance data schema for margin/cross margin accounts.

    Used by methods like fetch_balance (when in margin mode).

    Returns balance information for margin accounts with separate base/quote
    currency balances and debt tracking per trading pair.
    """

    # Required fields
    symbol: Series[str] = pa.Field(title="Symbol", description="Trading pair")
    base_free: Series[float] = pa.Field(
        ge=0, title="Base Free", description="Available base currency"
    )
    base_used: Series[float] = pa.Field(
        ge=0, title="Base Used", description="Base currency in open orders"
    )
    base_total: Series[float] = pa.Field(
        ge=0, title="Base Total", description="Total base currency"
    )
    quote_free: Series[float] = pa.Field(
        ge=0, title="Quote Free", description="Available quote currency"
    )
    quote_used: Series[float] = pa.Field(
        ge=0, title="Quote Used", description="Quote currency in open orders"
    )
    quote_total: Series[float] = pa.Field(
        ge=0, title="Quote Total", description="Total quote currency"
    )

    # Optional fields
    base_debt: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Base Debt", description="Borrowed base currency"
    )
    quote_debt: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Quote Debt", description="Borrowed quote currency"
    )
    base: Series[str] | None = pa.Field(
        nullable=True, title="Base", description="Base currency identifier"
    )
    quote: Series[str] | None = pa.Field(
        nullable=True, title="Quote", description="Quote currency identifier"
    )
    timestamp: Series[pd.Timestamp] | None = pa.Field(
        nullable=True, title="Timestamp", description="Balance snapshot timestamp"
    )
    datetime: Series[pd.Timestamp] | None = pa.Field(
        nullable=True, title="Datetime", description="Balance snapshot datetime (alias)"
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
