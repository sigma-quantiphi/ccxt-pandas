"""Order schema for order submission and validation."""

from typing import Optional

import pandera.pandas as pa

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class OrderSchema(BaseExchangeSchema):
    """Order schema for any exchange.

    Used for validating order DataFrames before submission via
    create_order_from_dataframe and similar methods.
    """

    id: Optional[str] = pa.Field(
        nullable=True, default=None, description="Exchange-assigned order ID"
    )
    symbol: str = pa.Field(description="Unified CCXT market symbol")
    side: str = pa.Field(isin=["buy", "sell"])
    type: str = pa.Field(isin=["limit", "market", "stop_loss", "take_profit"])
    amount: Optional[float] = pa.Field(gt=0)
    price: Optional[float] = pa.Field(ge=0, nullable=True, default=None)
    params: Optional[dict] = pa.Field(nullable=True, default=None)
