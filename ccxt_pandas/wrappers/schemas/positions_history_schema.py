"""Positions history data schema."""

from typing import Optional

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class PositionsHistorySchema(BaseExchangeSchema):
    """Positions history data schema.

    Used by methods like fetch_positions_history.

    Returns historical (closed) positions for derivatives contracts including
    entry/exit details and realized PnL.
    """

    # Required fields
    id: Series[str] = pa.Field(
        title="Position ID", description="Unique position identifier"
    )
    symbol: Series[str] = pa.Field(
        title="Symbol", description="Trading pair"
    )
    marginMode: Series[str] = pa.Field(
        isin=["cross", "isolated"], title="Margin Mode", description="Margin mode: 'cross' or 'isolated'"
    )
    entryPrice: Series[float] = pa.Field(
        ge=0, title="Entry Price", description="Average entry price of the position"
    )
    realizedPnl: Series[float] = pa.Field(
        title="Realized PnL", description="Realized profit and loss"
    )
    contractSize: Series[float] = pa.Field(
        ge=0, title="Contract Size", description="Size of each contract"
    )
    lastPrice: Series[float] = pa.Field(
        ge=0, title="Last Price", description="Last price when position was closed"
    )
    side: Series[str] = pa.Field(
        isin=["long", "short"], title="Side", description="Position side: 'long' or 'short'"
    )
    hedged: Series[bool] = pa.Field(
        title="Hedged", description="Whether position was in hedge mode"
    )
    timestamp: Series[pd.Timestamp] = pa.Field(
        title="Timestamp", description="Position open timestamp"
    )
    datetime: Series[pd.Timestamp] = pa.Field(
        title="Datetime", description="Position open datetime (alias)"
    )
    lastUpdateTimestamp: Series[pd.Timestamp] = pa.Field(
        title="Last Update Timestamp", description="Position close/update timestamp"
    )
    maintenanceMarginPercentage: Series[float] = pa.Field(
        ge=0, title="Maintenance Margin %", description="Maintenance margin percentage"
    )
    leverage: Series[float] = pa.Field(
        ge=0, title="Leverage", description="Position leverage"
    )

    # Optional fields
    initialMarginPercentage: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Initial Margin %", description="Initial margin percentage"
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
