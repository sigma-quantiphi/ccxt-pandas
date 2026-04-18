"""Liquidations data schema."""


import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class LiquidationsSchema(BaseExchangeSchema):
    """Liquidations data schema.

    Used by methods like fetch_liquidations.

    Returns liquidation events for derivatives contracts, showing forced closures
    of positions due to insufficient margin.
    """

    # Required fields
    symbol: Series[str] = pa.Field(title="Symbol", description="Trading pair")
    contracts: Series[float] = pa.Field(
        ge=0, title="Contracts", description="Number of contracts liquidated"
    )
    price: Series[float] = pa.Field(ge=0, title="Price", description="Liquidation price")
    timestamp: Series[pd.Timestamp] = pa.Field(
        title="Timestamp", description="Liquidation timestamp"
    )
    datetime: Series[pd.Timestamp] = pa.Field(
        title="Datetime", description="Liquidation datetime (alias)"
    )

    # Optional fields (not present in all exchanges)
    side: Series[str] | None = pa.Field(
        isin=["buy", "sell"],
        nullable=True,
        title="Side",
        description="Liquidation side: 'buy' or 'sell'",
    )
    baseValue: Series[float] | None = pa.Field(
        ge=0,
        nullable=True,
        title="Base Value",
        description="Liquidation value in base currency",
    )
    quoteValue: Series[float] | None = pa.Field(
        ge=0,
        nullable=True,
        title="Quote Value",
        description="Liquidation value in quote currency",
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
