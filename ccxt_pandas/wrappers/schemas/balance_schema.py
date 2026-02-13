"""Balance and wallet data schema."""

from typing import Optional

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class BalanceSchema(BaseExchangeSchema):
    """Balance/wallet data schema for spot balances.

    Used by methods like fetch_balance, watch_balance.

    Returns balance information for spot/wallet accounts with currency code
    and balance amounts (free, used, total, debt).
    """

    # Required fields
    code: Series[str] = pa.Field(title="Code", description="Currency code")
    free: Series[float] = pa.Field(
        ge=0, title="Free", description="Available balance"
    )
    used: Series[float] = pa.Field(
        ge=0, title="Used", description="Balance in open orders"
    )
    total: Series[float] = pa.Field(
        ge=0, title="Total", description="Total balance (free + used)"
    )

    # Optional fields
    debt: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Debt", description="Borrowed amount (margin)"
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
