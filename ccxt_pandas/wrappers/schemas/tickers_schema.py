"""Tickers data schema."""

from typing import Optional

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
    symbol: Series[str] = pa.Field(
        unique=True, title="Symbol", description="Trading pair"
    )

    # Optional timestamp fields
    timestamp: Optional[Series[pd.Timestamp]] = pa.Field(
        nullable=True, title="Timestamp", description="Ticker timestamp"
    )
    datetime: Optional[Series[pd.Timestamp]] = pa.Field(
        nullable=True, title="Datetime", description="Ticker datetime (alias)"
    )

    # Optional price fields
    open: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Open", description="24h opening price"
    )
    high: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="High", description="24h highest price"
    )
    low: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Low", description="24h lowest price"
    )
    close: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Close", description="Last closing price"
    )
    last: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Last", description="Last traded price"
    )
    bid: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Bid", description="Best bid price"
    )
    ask: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Ask", description="Best ask price"
    )
    vwap: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="VWAP", description="Volume weighted average price"
    )
    previousClose: Optional[Series[float]] = pa.Field(
        ge=0,
        nullable=True,
        title="Previous Close",
        description="Previous closing price",
    )
    average: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Average", description="Average price"
    )

    # Optional derivatives price fields
    markPrice: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Mark Price", description="Mark price (derivatives)"
    )
    indexPrice: Optional[Series[float]] = pa.Field(
        ge=0,
        nullable=True,
        title="Index Price",
        description="Index price (derivatives)",
    )

    # Optional change fields
    change: Optional[Series[float]] = pa.Field(
        nullable=True, title="Change", description="24h absolute price change"
    )
    percentage: Optional[Series[float]] = pa.Field(
        nullable=True, title="Percentage", description="24h percentage change"
    )

    # Optional volume fields
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
    bidVolume: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Bid Volume", description="Volume at best bid"
    )
    askVolume: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Ask Volume", description="Volume at best ask"
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
