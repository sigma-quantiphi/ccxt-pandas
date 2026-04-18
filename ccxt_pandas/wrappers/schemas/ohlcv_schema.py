"""OHLCV (candlestick) data schema."""

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class OHLCVSchema(BaseExchangeSchema):
    """OHLCV candlestick data schema.

    Used by methods like fetch_ohlcv, watch_ohlcv.

    All OHLCV fields (timestamp, OHLC prices, volume) are required.
    Symbol is optional as it may not be present in single-symbol queries.
    """

    timestamp: Series[pd.Timestamp] = pa.Field(title="Timestamp", description="Opening time (UTC)")
    open: Series[float] = pa.Field(ge=0, title="Open", description="Opening price")
    high: Series[float] = pa.Field(ge=0, title="High", description="Highest price")
    low: Series[float] = pa.Field(ge=0, title="Low", description="Lowest price")
    close: Series[float] = pa.Field(ge=0, title="Close", description="Closing price")
    volume: Series[float] = pa.Field(ge=0, title="Volume", description="Volume")
    symbol: Series[str] | None = pa.Field(
        nullable=True,
        title="Symbol",
        description="Trading pair (optional for single-symbol queries)",
    )
