"""Borrow rates data schemas for cross and isolated margin."""

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
    rate: Series[float] = pa.Field(ge=0, title="Rate", description="Borrow interest rate")
    period: Series[int] = pa.Field(ge=0, title="Period", description="Rate period in milliseconds")
    # Note: exchange field comes from BaseExchangeSchema (Optional)


class IsolatedBorrowRatesSchema(BaseExchangeSchema):
    """Isolated borrow rates data schema.

    Used by methods like fetch_isolated_borrow_rates.

    Returns borrowing interest rates for isolated-margin trading pairs, showing
    separate rates for base and quote currencies.
    """

    # Required fields
    symbol: Series[str] = pa.Field(title="Symbol", description="Trading pair")
    base: Series[str] = pa.Field(title="Base", description="Base currency")
    baseRate: Series[float] = pa.Field(
        ge=0, title="Base Rate", description="Borrow interest rate for base currency"
    )
    quote: Series[str] = pa.Field(title="Quote", description="Quote currency")
    quoteRate: Series[float] = pa.Field(
        ge=0, title="Quote Rate", description="Borrow interest rate for quote currency"
    )
    period: Series[int] = pa.Field(ge=0, title="Period", description="Rate period in milliseconds")
    # Note: exchange field comes from BaseExchangeSchema (Optional)
