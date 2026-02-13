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
from ccxt_pandas.wrappers.schemas.funding_rate_history_schema import FundingRateHistorySchema
from ccxt_pandas.wrappers.schemas.greeks_schema import GreeksSchema
from ccxt_pandas.wrappers.schemas.last_prices_schema import LastPricesSchema
from ccxt_pandas.wrappers.schemas.liquidations_schema import LiquidationsSchema
from ccxt_pandas.wrappers.schemas.long_short_ratio_schema import LongShortRatioSchema
from ccxt_pandas.wrappers.schemas.mark_prices_schema import MarkPricesSchema
from ccxt_pandas.wrappers.schemas.market_schema import MarketSchema
from ccxt_pandas.wrappers.schemas.my_trades_schema import MyTradesSchema
from ccxt_pandas.wrappers.schemas.ohlcv_schema import OHLCVSchema
from ccxt_pandas.wrappers.schemas.open_interest_history_schema import OpenInterestHistorySchema
from ccxt_pandas.wrappers.schemas.order_schema import OrderSchema
from ccxt_pandas.wrappers.schemas.order_book_schema import OrderBookSchema
from ccxt_pandas.wrappers.schemas.tickers_schema import TickersSchema
from ccxt_pandas.wrappers.schemas.trade_schema import TradeSchema
from ccxt_pandas.wrappers.schemas.volatility_history_schema import VolatilityHistorySchema

__all__ = [
    "BaseExchangeSchema",
    "OrderSchema",
    "OHLCVSchema",
    "BalanceSchema",
    "MarketSchema",
    "CurrencySchema",
    "OrderBookSchema",
    "TickersSchema",
    "TradeSchema",
    "BidsAsksSchema",
    "FundingRateSchema",
    "FundingRateHistorySchema",
    "GreeksSchema",
    "LastPricesSchema",
    "LiquidationsSchema",
    "LongShortRatioSchema",
    "MarkPricesSchema",
    "MyTradesSchema",
    "OpenInterestHistorySchema",
    "VolatilityHistorySchema",
]
