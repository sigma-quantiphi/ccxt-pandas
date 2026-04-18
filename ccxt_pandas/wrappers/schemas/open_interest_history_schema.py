"""Open interest history data schema."""


import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class OpenInterestHistorySchema(BaseExchangeSchema):
    """Open interest history data schema.

    Used by methods like fetch_open_interest_history.

    Returns historical open interest data for derivatives contracts.
    """

    # Required fields
    symbol: Series[str] = pa.Field(title="Symbol", description="Trading pair")
    openInterestAmount: Series[float] = pa.Field(
        ge=0, title="Open Interest Amount", description="Open interest in base currency"
    )

    # Optional volume fields
    baseVolume: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Base Volume", description="Volume in base currency"
    )
    quoteVolume: Series[float] | None = pa.Field(
        ge=0,
        nullable=True,
        title="Quote Volume",
        description="Volume in quote currency",
    )

    # Optional open interest value
    openInterestValue: Series[float] | None = pa.Field(
        ge=0,
        nullable=True,
        title="Open Interest Value",
        description="Open interest in quote currency value",
    )

    timestamp: Series[pd.Timestamp] | None = pa.Field(
        nullable=False, title="Timestamp", description="Open interest timestamp"
    )
    datetime: Series[pd.Timestamp] | None = pa.Field(
        nullable=False, title="Datetime", description="Open interest datetime (alias)"
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
