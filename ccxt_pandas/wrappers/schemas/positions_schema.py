"""Positions data schema."""

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class PositionsSchema(BaseExchangeSchema):
    """Positions data schema.

    Used by methods like fetch_positions, fetch_position.

    Returns open positions for derivatives contracts including margin details,
    PnL, and risk metrics.
    """

    # Required fields
    id: Series[str] = pa.Field(
        title="Position ID", description="Unique position identifier"
    )
    symbol: Series[str] = pa.Field(
        title="Symbol", description="Trading pair"
    )
    notional: Series[float] = pa.Field(
        ge=0, title="Notional", description="Notional value of the position"
    )
    marginMode: Series[str] = pa.Field(
        isin=["cross", "isolated"], title="Margin Mode", description="Margin mode: 'cross' or 'isolated'"
    )
    liquidationPrice: Series[float] = pa.Field(
        ge=0, title="Liquidation Price", description="Price at which position will be liquidated"
    )
    entryPrice: Series[float] = pa.Field(
        ge=0, title="Entry Price", description="Average entry price of the position"
    )
    unrealizedPnl: Series[float] = pa.Field(
        title="Unrealized PnL", description="Unrealized profit and loss"
    )
    realizedPnl: Series[float] = pa.Field(
        title="Realized PnL", description="Realized profit and loss"
    )
    percentage: Series[float] = pa.Field(
        title="Percentage", description="PnL percentage"
    )
    contracts: Series[float] = pa.Field(
        ge=0, title="Contracts", description="Number of contracts"
    )
    contractSize: Series[float] = pa.Field(
        ge=0, title="Contract Size", description="Size of each contract"
    )
    markPrice: Series[float] = pa.Field(
        ge=0, title="Mark Price", description="Current mark price"
    )
    side: Series[str] = pa.Field(
        isin=["long", "short"], title="Side", description="Position side: 'long' or 'short'"
    )
    hedged: Series[bool] = pa.Field(
        title="Hedged", description="Whether position is in hedge mode"
    )
    timestamp: Series[pd.Timestamp] = pa.Field(
        title="Timestamp", description="Position open timestamp"
    )
    datetime: Series[pd.Timestamp] = pa.Field(
        title="Datetime", description="Position open datetime (alias)"
    )
    lastUpdateTimestamp: Series[pd.Timestamp] = pa.Field(
        title="Last Update Timestamp", description="Last position update timestamp"
    )
    maintenanceMargin: Series[float] = pa.Field(
        ge=0, title="Maintenance Margin", description="Maintenance margin amount"
    )
    maintenanceMarginPercentage: Series[float] = pa.Field(
        ge=0, title="Maintenance Margin %", description="Maintenance margin percentage"
    )
    collateral: Series[float] = pa.Field(
        ge=0, title="Collateral", description="Collateral amount"
    )
    initialMargin: Series[float] = pa.Field(
        ge=0, title="Initial Margin", description="Initial margin amount"
    )
    initialMarginPercentage: Series[float] = pa.Field(
        ge=0, title="Initial Margin %", description="Initial margin percentage"
    )
    leverage: Series[float] = pa.Field(
        ge=0, title="Leverage", description="Position leverage"
    )
    marginRatio: Series[float] = pa.Field(
        ge=0, title="Margin Ratio", description="Current margin ratio"
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
