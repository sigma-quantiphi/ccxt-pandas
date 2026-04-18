"""Tickers data schema."""


import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class TickersSchema(BaseExchangeSchema):
    """Tickers data schema.

    Used by methods like fetch_tickers, fetch_ticker.

    Returns 24-hour ticker statistics for trading pairs including price,
    volume, and percentage changes.
    """

    # Required fields
    symbol: Series[str] = pa.Field(unique=True, title="Symbol", description="Trading pair")

    # Optional timestamp fields
    timestamp: Series[pd.Timestamp] | None = pa.Field(
        nullable=True, title="Timestamp", description="Ticker timestamp"
    )
    datetime: Series[pd.Timestamp] | None = pa.Field(
        nullable=True, title="Datetime", description="Ticker datetime (alias)"
    )

    # Optional price fields
    open: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Open", description="24h opening price"
    )
    high: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="High", description="24h highest price"
    )
    low: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Low", description="24h lowest price"
    )
    close: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Close", description="Last closing price"
    )
    last: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Last", description="Last traded price"
    )
    bid: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Bid", description="Best bid price"
    )
    ask: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Ask", description="Best ask price"
    )
    vwap: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="VWAP", description="Volume weighted average price"
    )
    previousClose: Series[float] | None = pa.Field(
        ge=0,
        nullable=True,
        title="Previous Close",
        description="Previous closing price",
    )
    average: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Average", description="Average price"
    )

    # Optional derivatives price fields
    markPrice: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Mark Price", description="Mark price (derivatives)"
    )
    indexPrice: Series[float] | None = pa.Field(
        ge=0,
        nullable=True,
        title="Index Price",
        description="Index price (derivatives)",
    )

    # Optional change fields
    change: Series[float] | None = pa.Field(
        nullable=True, title="Change", description="24h absolute price change"
    )
    percentage: Series[float] | None = pa.Field(
        nullable=True, title="Percentage", description="24h percentage change"
    )

    # Optional volume fields
    baseVolume: Series[float] | None = pa.Field(
        ge=0,
        nullable=True,
        title="Base Volume",
        description="24h volume in base currency",
    )
    quoteVolume: Series[float] | None = pa.Field(
        ge=0,
        nullable=True,
        title="Quote Volume",
        description="24h volume in quote currency",
    )
    bidVolume: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Bid Volume", description="Volume at best bid"
    )
    askVolume: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Ask Volume", description="Volume at best ask"
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
