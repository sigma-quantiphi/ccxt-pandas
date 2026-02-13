"""Long/short ratio data schema."""

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class LongShortRatioSchema(BaseExchangeSchema):
    """Long/short ratio data schema.

    Used by methods like fetch_long_short_ratio.

    Returns the ratio of long positions to short positions for a trading pair.
    """

    # Required fields
    symbol: Series[str] = pa.Field(title="Symbol", description="Trading pair")
    timestamp: Series[pd.Timestamp] = pa.Field(
        title="Timestamp", description="Long/short ratio timestamp"
    )
    datetime: Series[pd.Timestamp] = pa.Field(
        title="Datetime", description="Long/short ratio datetime (alias)"
    )
    longShortRatio: Series[float] = pa.Field(
        ge=0,
        title="Long/Short Ratio",
        description="Ratio of long positions to short positions",
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
