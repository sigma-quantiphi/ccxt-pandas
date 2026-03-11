"""Borrow interest data schema."""

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class BorrowInterestSchema(BaseExchangeSchema):
    """Borrow interest data schema.

    Used by methods like fetch_borrow_interest.

    Returns historical borrow interest charges for margin/leveraged positions,
    showing the interest accrued on borrowed funds.
    """

    # Required fields
    account: Series[str] = pa.Field(
        title="Account", description="Market symbol that the interest was accrued in"
    )
    currency: Series[str] = pa.Field(
        title="Currency", description="Currency of the interest"
    )
    interest: Series[float] = pa.Field(
        ge=0, title="Interest", description="Amount of interest charged"
    )
    interestRate: Series[float] = pa.Field(
        ge=0, title="Interest Rate", description="Borrow interest rate"
    )
    amountBorrowed: Series[float] = pa.Field(
        ge=0,
        title="Amount Borrowed",
        description="Amount of currency that was borrowed",
    )
    timestamp: Series[pd.Timestamp] = pa.Field(
        title="Timestamp", description="Timestamp when interest was charged"
    )
    datetime: Series[pd.Timestamp] = pa.Field(
        title="Datetime", description="Datetime when interest was charged (alias)"
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
