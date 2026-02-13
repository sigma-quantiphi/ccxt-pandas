"""Trading fees data schema."""

import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class TradingFeesSchema(BaseExchangeSchema):
    """Trading fees data schema.

    Used by methods like fetch_trading_fees.

    Returns maker and taker fee rates for each trading pair.
    """

    # Required fields
    symbol: Series[str] = pa.Field(
        title="Symbol", description="Trading pair"
    )
    maker: Series[float] = pa.Field(
        ge=0, title="Maker", description="Maker fee rate"
    )
    taker: Series[float] = pa.Field(
        ge=0, title="Taker", description="Taker fee rate"
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
