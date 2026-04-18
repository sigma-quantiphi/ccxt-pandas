"""Funding rate history data schema."""

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class FundingRateHistorySchema(BaseExchangeSchema):
    """Funding rate history data schema.

    Used by methods like fetch_funding_rate_history.

    Returns historical funding rate data over time.
    Requires symbol, fundingRate, and timestamps.
    """

    # Required fields
    symbol: Series[str] = pa.Field(title="Symbol", description="Trading pair")
    fundingRate: Series[float] = pa.Field(
        title="Funding Rate", description="Historical funding rate"
    )
    timestamp: Series[pd.Timestamp] = pa.Field(
        title="Timestamp", description="Funding rate timestamp"
    )
    datetime: Series[pd.Timestamp] = pa.Field(
        title="Datetime", description="Funding rate datetime (alias)"
    )

    # Optional fields
    markPrice: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Mark Price", description="Mark price at this time"
    )
    indexPrice: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Index Price", description="Index price at this time"
    )
    nextFundingRate: Series[float] | None = pa.Field(
        nullable=True, title="Next Funding Rate", description="Next funding rate"
    )
    nextFundingTimestamp: Series[pd.Timestamp] | None = pa.Field(
        nullable=True, title="Next Funding Time", description="Next funding timestamp"
    )
    nextFundingDatetime: Series[pd.Timestamp] | None = pa.Field(
        nullable=True,
        title="Next Funding Datetime",
        description="Next funding datetime (alias)",
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
