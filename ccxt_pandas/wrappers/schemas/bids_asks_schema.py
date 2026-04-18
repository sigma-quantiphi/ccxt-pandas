"""Bids/Asks ticker data schema."""

import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class BidsAsksSchema(BaseExchangeSchema):
    """Bids/Asks ticker data schema.

    Used by methods like fetch_bids_asks.

    Returns best bid/ask prices with volumes and optional ticker data.
    """

    # Required fields
    symbol: Series[str] = pa.Field(unique=True, title="Symbol", description="Trading pair")
    # Bid/ask can be null if orderbook is empty
    bid: Series[float] = pa.Field(
        ge=0,
        nullable=True,
        title="Bid",
        description="Best bid price (null if orderbook empty)",
    )
    bidVolume: Series[float] = pa.Field(
        ge=0,
        nullable=True,
        title="Bid Volume",
        description="Volume at best bid (null if orderbook empty)",
    )
    ask: Series[float] = pa.Field(
        ge=0,
        nullable=True,
        title="Ask",
        description="Best ask price (null if orderbook empty)",
    )
    askVolume: Series[float] = pa.Field(
        ge=0,
        nullable=True,
        title="Ask Volume",
        description="Volume at best ask (null if orderbook empty)",
    )

    # Optional ticker fields
    high: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="24h High", description="24h highest price"
    )
    low: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="24h Low", description="24h lowest price"
    )
    vwap: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="VWAP", description="Volume-weighted average price"
    )
    open: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Open", description="Opening price"
    )
    close: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Close", description="Closing price"
    )
    last: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Last", description="Last trade price"
    )
    change: Series[float] | None = pa.Field(
        nullable=True, title="Change", description="Price change"
    )
    percentage: Series[float] | None = pa.Field(
        nullable=True, title="Percentage", description="Percentage change"
    )
    average: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Average", description="Average price"
    )
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
    markPrice: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Mark Price", description="Mark price (derivatives)"
    )
    indexPrice: Series[float] | None = pa.Field(
        ge=0,
        nullable=True,
        title="Index Price",
        description="Index price (derivatives)",
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
