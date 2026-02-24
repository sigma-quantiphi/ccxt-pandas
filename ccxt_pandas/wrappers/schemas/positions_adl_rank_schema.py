"""Positions ADL (Auto De-Leverage) rank schema."""

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class PositionsADLRankSchema(BaseExchangeSchema):
    """Positions ADL (Auto De-Leverage) rank schema.

    Used by fetch_positions_adl_rank.

    Returns the ADL risk ranking for each position, indicating the likelihood
    of auto-deleveraging. A higher rank/percent means higher ADL risk.
    """

    symbol: Series[str] = pa.Field(title="Symbol", description="Unified CCXT market symbol")
    rank: Series[int] = pa.Field(
        ge=1,
        le=5,
        title="Rank",
        description="Quantile rank from 1 to 5, with 5 being the highest ADL risk",
    )
    rating: Series[str] = pa.Field(
        title="Rating",
        description="Risk rating: low, medium, or high",
        isin=["low", "medium", "high"],
    )
    percent: Series[float] = pa.Field(
        ge=0,
        le=100,
        title="Percent",
        description="Risk percentage; higher values indicate higher risk of auto-deleveraging",
    )
    timestamp: Series[pd.Timestamp] = pa.Field(
        title="Timestamp", description="Unix timestamp in milliseconds"
    )
    datetime: Series[pd.Timestamp] = pa.Field(
        title="Datetime", description="ISO8601 datetime with milliseconds"
    )