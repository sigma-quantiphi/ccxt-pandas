"""Leverages data schema."""

import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class LeveragesSchema(BaseExchangeSchema):
    """Leverages data schema.

    Used by methods like fetch_leverages.

    Returns maximum leverage available for each trading pair, with separate
    limits for long and short positions.
    """

    # Required fields
    symbol: Series[str] = pa.Field(
        title="Symbol", description="Trading pair"
    )
    marginMode: Series[str] = pa.Field(
        isin=["cross", "isolated"], title="Margin Mode", description="Margin mode: 'cross' or 'isolated'"
    )
    longLeverage: Series[int] = pa.Field(
        ge=1, title="Long Leverage", description="Maximum leverage for long positions"
    )
    shortLeverage: Series[int] = pa.Field(
        ge=1, title="Short Leverage", description="Maximum leverage for short positions"
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
