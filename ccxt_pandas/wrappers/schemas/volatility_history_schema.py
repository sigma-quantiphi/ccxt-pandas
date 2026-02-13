"""Volatility history data schema."""

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class VolatilityHistorySchema(BaseExchangeSchema):
    """Volatility history data schema.

    Used by methods like fetch_volatility_history.

    Returns historical volatility data for a trading pair, typically used
    in options pricing and risk management.
    """

    # Required fields
    timestamp: Series[pd.Timestamp] = pa.Field(
        title="Timestamp", description="Volatility measurement timestamp"
    )
    datetime: Series[pd.Timestamp] = pa.Field(
        title="Datetime", description="Volatility measurement datetime (alias)"
    )
    volatility: Series[float] = pa.Field(
        ge=0, title="Volatility", description="Historical volatility value"
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
