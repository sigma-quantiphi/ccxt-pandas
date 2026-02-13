"""Cross borrow rates data schema."""

import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class CrossBorrowRatesSchema(BaseExchangeSchema):
    """Cross borrow rates data schema.

    Used by methods like fetch_cross_borrow_rates.

    Returns borrowing interest rates for cross-margin trading, showing the cost
    of borrowing assets for margin positions.
    """

    # Required fields
    currency: Series[str] = pa.Field(
        title="Currency", description="Currency code (e.g., BTC, USDT)"
    )
    rate: Series[float] = pa.Field(
        ge=0, title="Rate", description="Borrow interest rate"
    )
    period: Series[int] = pa.Field(
        ge=0, title="Period", description="Rate period in milliseconds"
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
