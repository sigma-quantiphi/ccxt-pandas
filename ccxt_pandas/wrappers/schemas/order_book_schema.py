"""Order book data schema."""

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class OrderBookSchema(BaseExchangeSchema):
    """Order book data schema.

    Used by methods like fetch_order_book, watch_order_book.

    Order books are returned as DataFrames with bids and asks combined,
    differentiated by the 'side' column.
    """

    price: Series[float] = pa.Field(ge=0, nullable=True, title="Price", description="Price level")
    qty: Series[float] = pa.Field(
        ge=0,
        nullable=True,
        title="Quantity",
        description="Quantity at this price level",
    )
    side: Series[str] = pa.Field(
        nullable=True,
        isin=["bids", "asks"],
        title="Side",
        description="Side: 'bids' or 'asks'",
    )
    symbol: Series[str] | None = pa.Field(nullable=True, title="Symbol", description="Trading pair")
    timestamp: Series[pd.Timestamp] | None = pa.Field(
        nullable=True, title="Timestamp", description="Order book timestamp"
    )
    datetime: Series[pd.Timestamp] | None = pa.Field(
        nullable=True, title="Datetime", description="Order book datetime (alias)"
    )
    nonce: Series[int] | None = pa.Field(
        nullable=True, title="Nonce", description="Order book sequence number"
    )
