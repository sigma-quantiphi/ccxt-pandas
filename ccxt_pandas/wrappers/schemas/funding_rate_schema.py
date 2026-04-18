"""Funding rate data schema."""

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class FundingRateSchema(BaseExchangeSchema):
    """Funding rate data schema.

    Used by methods like fetch_funding_rates.

    Returns current and historical funding rates for perpetual swap contracts.
    Only symbol and fundingRate are required, all other fields are optional.
    """

    # Required fields
    symbol: Series[str] = pa.Field(unique=True, title="Symbol", description="Trading pair")
    fundingRate: Series[float] = pa.Field(title="Funding Rate", description="Current funding rate")

    # Optional price fields
    markPrice: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Mark Price", description="Current mark price"
    )
    indexPrice: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Index Price", description="Current index price"
    )
    estimatedSettlePrice: Series[float] | None = pa.Field(
        ge=0,
        nullable=True,
        title="Est. Settle Price",
        description="Estimated settlement price",
    )

    # Optional rate fields
    interestRate: Series[float] | None = pa.Field(
        nullable=True, title="Interest Rate", description="Interest rate component"
    )
    nextFundingRate: Series[float] | None = pa.Field(
        nullable=True, title="Next Funding Rate", description="Next funding rate"
    )
    previousFundingRate: Series[float] | None = pa.Field(
        nullable=True, title="Prev Funding Rate", description="Previous funding rate"
    )

    # Optional timestamp fields
    timestamp: Series[pd.Timestamp] | None = pa.Field(
        nullable=True, title="Timestamp", description="Current timestamp"
    )
    datetime: Series[pd.Timestamp] | None = pa.Field(
        nullable=True, title="Datetime", description="Current datetime (alias)"
    )
    fundingTimestamp: Series[pd.Timestamp] | None = pa.Field(
        nullable=True,
        title="Funding Timestamp",
        description="Current funding timestamp",
    )
    fundingDatetime: Series[pd.Timestamp] | None = pa.Field(
        nullable=True,
        title="Funding Datetime",
        description="Current funding datetime (alias)",
    )
    nextFundingTimestamp: Series[pd.Timestamp] | None = pa.Field(
        nullable=True, title="Next Funding Time", description="Next funding timestamp"
    )
    nextFundingDatetime: Series[pd.Timestamp] | None = pa.Field(
        nullable=True,
        title="Next Funding Datetime",
        description="Next funding datetime (alias)",
    )
    previousFundingTimestamp: Series[pd.Timestamp] | None = pa.Field(
        nullable=True,
        title="Prev Funding Time",
        description="Previous funding timestamp",
    )
    previousFundingDatetime: Series[pd.Timestamp] | None = pa.Field(
        nullable=True,
        title="Prev Funding Datetime",
        description="Previous funding datetime (alias)",
    )

    # Optional metadata
    interval: Series[str] | None = pa.Field(
        nullable=True, title="Interval", description="Funding interval period"
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
