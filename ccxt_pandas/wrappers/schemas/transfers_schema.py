"""Transfers data schema."""

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class TransfersSchema(BaseExchangeSchema):
    """Transfers data schema.

    Used by methods like fetch_transfers.

    Returns internal transfer history between user accounts (e.g., trading to funding,
    spot to futures).
    """

    # Required fields
    id: Series[str] = pa.Field(title="Transfer ID", description="Unique transfer identifier")
    timestamp: Series[pd.Timestamp] = pa.Field(title="Timestamp", description="Transfer timestamp")
    datetime: Series[pd.Timestamp] = pa.Field(
        title="Datetime", description="Transfer datetime (alias)"
    )
    currency: Series[str] = pa.Field(title="Currency", description="Currency transferred")
    amount: Series[float] = pa.Field(ge=0, title="Amount", description="Transfer amount")
    fromAccount: Series[str] = pa.Field(title="From Account", description="Source account type")
    toAccount: Series[str] = pa.Field(title="To Account", description="Destination account type")
    code: Series[str] = pa.Field(title="Code", description="Currency code")
    # Note: exchange field comes from BaseExchangeSchema (Optional)
