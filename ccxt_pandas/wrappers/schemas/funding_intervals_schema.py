"""Funding intervals data schema."""

import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class FundingIntervalsSchema(BaseExchangeSchema):
    """Funding intervals data schema.

    Used by methods like fetch_funding_intervals.

    Returns the funding rate payment interval for derivatives contracts,
    indicating how often funding payments are made (e.g., 8h, 4h).
    """

    # Required fields
    symbol: Series[str] = pa.Field(title="Symbol", description="Trading pair")
    interval: Series[str] = pa.Field(
        title="Interval", description="Funding payment interval (e.g., 8h, 4h, 1h)"
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
