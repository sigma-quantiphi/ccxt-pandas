"""Bids/Asks ticker data schema."""

from typing import Optional

import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class BidsAsksSchema(BaseExchangeSchema):
    """Bids/Asks ticker data schema.

    Used by methods like fetch_bids_asks.

    Returns best bid/ask prices with volumes and optional ticker data.
    """

    # Required fields
    symbol: Series[str] = pa.Field(
        unique=True, title="Symbol", description="Trading pair"
    )
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
    high: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="24h High", description="24h highest price"
    )
    low: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="24h Low", description="24h lowest price"
    )
    vwap: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="VWAP", description="Volume-weighted average price"
    )
    open: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Open", description="Opening price"
    )
    close: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Close", description="Closing price"
    )
    last: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Last", description="Last trade price"
    )
    change: Optional[Series[float]] = pa.Field(
        nullable=True, title="Change", description="Price change"
    )
    percentage: Optional[Series[float]] = pa.Field(
        nullable=True, title="Percentage", description="Percentage change"
    )
    average: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Average", description="Average price"
    )
    baseVolume: Optional[Series[float]] = pa.Field(
        ge=0,
        nullable=True,
        title="Base Volume",
        description="24h volume in base currency",
    )
    quoteVolume: Optional[Series[float]] = pa.Field(
        ge=0,
        nullable=True,
        title="Quote Volume",
        description="24h volume in quote currency",
    )
    markPrice: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Mark Price", description="Mark price (derivatives)"
    )
    indexPrice: Optional[Series[float]] = pa.Field(
        ge=0,
        nullable=True,
        title="Index Price",
        description="Index price (derivatives)",
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
