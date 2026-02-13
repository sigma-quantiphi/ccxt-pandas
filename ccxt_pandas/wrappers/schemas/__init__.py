"""Pandera schemas for ccxt-pandas DataFrame responses.

This package provides comprehensive schema definitions for all DataFrame types
returned by ccxt-pandas methods. These schemas serve as:

- Documentation of DataFrame structures
- Type hints for IDE autocomplete (future)
- Runtime validation (optional, future)

All schemas inherit from BaseExchangeSchema and use permissive validation
(most fields optional, strict=False) to handle exchange-specific variations.
"""

from ccxt_pandas.wrappers.schemas.balance_schema import BalanceSchema
from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema
from ccxt_pandas.wrappers.schemas.bids_asks_schema import BidsAsksSchema
from ccxt_pandas.wrappers.schemas.currency_schema import CurrencySchema
from ccxt_pandas.wrappers.schemas.funding_rate_schema import FundingRateSchema
from ccxt_pandas.wrappers.schemas.market_schema import MarketSchema
from ccxt_pandas.wrappers.schemas.ohlcv_schema import OHLCVSchema
from ccxt_pandas.wrappers.schemas.order_schema import OrderSchema
from ccxt_pandas.wrappers.schemas.orderbook_schema import OrderBookSchema
from ccxt_pandas.wrappers.schemas.trade_schema import TradeSchema

__all__ = [
    "BaseExchangeSchema",
    "OrderSchema",
    "OHLCVSchema",
    "BalanceSchema",
    "MarketSchema",
    "CurrencySchema",
    "OrderBookSchema",
    "TradeSchema",
    "BidsAsksSchema",
    "FundingRateSchema",
]
