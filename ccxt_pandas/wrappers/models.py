from typing import Literal

import ccxt
from pydantic import BaseModel, Field, SecretStr

SupportedExchanges = Literal[*ccxt.exchanges]


class ExchangeClientConfig(BaseModel):
    exchange: SupportedExchanges = Field(
        ..., description="Exchange must be one of the supported ccxt exchanges."
    )
    apiKey: str
    secret: SecretStr
    sandboxMode: bool = True
    model_config = {"extra": "allow"}
