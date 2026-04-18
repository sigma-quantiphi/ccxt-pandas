"""Options Greeks data schema."""

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class GreeksSchema(BaseExchangeSchema):
    """Options Greeks data schema.

    Used by methods like fetch_all_greeks, fetch_greeks.

    Returns option Greeks (delta, gamma, vega, theta, rho) and related pricing data.
    """

    # Required fields
    symbol: Series[str] = pa.Field(
        unique=True, title="Symbol", description="Option contract symbol"
    )
    delta: Series[float] = pa.Field(title="Delta", description="Option delta (price sensitivity)")
    gamma: Series[float] = pa.Field(title="Gamma", description="Option gamma (delta sensitivity)")
    vega: Series[float] = pa.Field(title="Vega", description="Option vega (volatility sensitivity)")
    markPrice: Series[float] = pa.Field(ge=0, title="Mark Price", description="Option mark price")

    # Optional Greeks
    theta: Series[float] | None = pa.Field(
        nullable=True, title="Theta", description="Option theta (time decay)"
    )
    rho: Series[float] | None = pa.Field(
        nullable=True, title="Rho", description="Option rho (interest rate sensitivity)"
    )

    # Optional implied volatility
    bidImpliedVolatility: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Bid IV", description="Bid implied volatility"
    )
    askImpliedVolatility: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Ask IV", description="Ask implied volatility"
    )
    markImpliedVolatility: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Mark IV", description="Mark implied volatility"
    )

    # Optional bid/ask data
    bidPrice: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Bid Price", description="Best bid price"
    )
    bidSize: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Bid Size", description="Best bid size"
    )
    askPrice: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Ask Price", description="Best ask price"
    )
    askSize: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Ask Size", description="Best ask size"
    )

    # Optional price data
    lastPrice: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Last Price", description="Last trade price"
    )
    underlyingPrice: Series[float] | None = pa.Field(
        ge=0,
        nullable=True,
        title="Underlying Price",
        description="Underlying asset price",
    )

    # Optional timestamps
    timestamp: Series[pd.Timestamp] | None = pa.Field(
        nullable=True, title="Timestamp", description="Greeks calculation timestamp"
    )
    datetime: Series[pd.Timestamp] | None = pa.Field(
        nullable=True,
        title="Datetime",
        description="Greeks calculation datetime (alias)",
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
