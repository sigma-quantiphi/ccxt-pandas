"""Portfolios data schema."""

import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class PortfoliosSchema(BaseExchangeSchema):
    """Portfolios data schema.

    Used by methods like fetch_portfolios.

    Returns user's portfolios or trading accounts on the exchange,
    such as default accounts, futures accounts, or other account types.
    """

    # Required fields
    id: Series[str] = pa.Field(title="Portfolio ID", description="Unique portfolio identifier")
    type: Series[str] = pa.Field(
        title="Type", description="Portfolio type (e.g., DEFAULT, INTX, FUTURES)"
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
