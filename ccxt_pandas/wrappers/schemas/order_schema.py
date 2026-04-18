"""Order schema for order submission and validation."""


import pandera.pandas as pa

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class OrderSchema(BaseExchangeSchema):
    """Order schema for any exchange.

    Used for validating order DataFrames before submission via
    create_order_from_dataframe and similar methods.
    """

    id: str | None = pa.Field(
        nullable=True, default=None, description="Exchange-assigned order ID"
    )
    symbol: str = pa.Field(description="Unified CCXT market symbol")
    side: str = pa.Field(isin=["buy", "sell"])
    type: str = pa.Field(isin=["limit", "market", "stop_loss", "take_profit", "LIMIT_MAKER"])
    amount: float | None = pa.Field(gt=0)
    price: float | None = pa.Field(ge=0, nullable=True, default=None)
    params: dict | None = pa.Field(nullable=True, default=None)
