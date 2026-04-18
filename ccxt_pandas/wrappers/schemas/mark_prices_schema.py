"""Mark prices data schema."""


import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class MarkPricesSchema(BaseExchangeSchema):
    """Mark prices data schema.

    Used by methods like fetch_mark_prices.

    Returns mark prices (and optionally index prices) for derivatives contracts.
    """

    # Required fields
    symbol: Series[str] = pa.Field(unique=True, title="Symbol", description="Trading pair")
    markPrice: Series[float] = pa.Field(ge=0, title="Mark Price", description="Current mark price")

    # Optional fields
    indexPrice: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Index Price", description="Current index price"
    )
    timestamp: Series[pd.Timestamp] | None = pa.Field(
        nullable=True, title="Timestamp", description="Mark price timestamp"
    )
    datetime: Series[pd.Timestamp] | None = pa.Field(
        nullable=True, title="Datetime", description="Mark price datetime (alias)"
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
