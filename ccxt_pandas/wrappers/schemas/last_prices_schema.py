"""Last prices data schema."""

from typing import Optional

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class LastPricesSchema(BaseExchangeSchema):
    """Last prices data schema.

    Used by methods like fetch_last_prices.

    Returns the last traded price for each symbol.
    """

    # Required fields
    symbol: Series[str] = pa.Field(
        unique=True, title="Symbol", description="Trading pair"
    )
    price: Series[float] = pa.Field(
        ge=0, title="Price", description="Last traded price"
    )

    # Optional timestamps
    timestamp: Optional[Series[pd.Timestamp]] = pa.Field(
        nullable=True, title="Timestamp", description="Last price timestamp"
    )
    datetime: Optional[Series[pd.Timestamp]] = pa.Field(
        nullable=True, title="Datetime", description="Last price datetime (alias)"
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
