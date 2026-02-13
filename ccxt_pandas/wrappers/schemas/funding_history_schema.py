"""Funding history data schema."""

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class FundingHistorySchema(BaseExchangeSchema):
    """Funding history data schema.

    Used by methods like fetch_funding_history.

    Returns historical funding payments for derivatives positions, showing amounts
    paid or received at each funding interval.
    """

    # Required fields
    symbol: Series[str] = pa.Field(title="Symbol", description="Trading pair")
    code: Series[str] = pa.Field(title="Code", description="Currency code (e.g., USDT)")
    timestamp: Series[pd.Timestamp] = pa.Field(
        title="Timestamp", description="Funding payment timestamp"
    )
    datetime: Series[pd.Timestamp] = pa.Field(
        title="Datetime", description="Funding payment datetime (alias)"
    )
    id: Series[str] = pa.Field(
        title="Funding ID", description="Unique funding payment identifier"
    )
    amount: Series[float] = pa.Field(
        title="Amount",
        description="Funding amount (negative if paid, positive if received)",
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
