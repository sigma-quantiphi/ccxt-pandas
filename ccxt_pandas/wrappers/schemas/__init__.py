"""Pandera schemas for ccxt-pandas DataFrame responses.

This package provides comprehensive schema definitions for all DataFrame types
returned by ccxt-pandas methods. These schemas serve as:

- Documentation of DataFrame structures
- Type hints for IDE autocomplete (future)
- Runtime validation (optional, future)

All schemas inherit from BaseExchangeSchema and use permissive validation
(most fields optional, strict=False) to handle exchange-specific variations.
"""

from ccxt_pandas.wrappers.schemas.accounts_schema import AccountsSchema
from ccxt_pandas.wrappers.schemas.addresses_schema import AddressesSchema
from ccxt_pandas.wrappers.schemas.balance_schema import BalanceSchema
from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema, FeeFieldsMixin
from ccxt_pandas.wrappers.schemas.bids_asks_schema import BidsAsksSchema
from ccxt_pandas.wrappers.schemas.borrow_interest_schema import BorrowInterestSchema
from ccxt_pandas.wrappers.schemas.borrow_rates_schema import (
    CrossBorrowRatesSchema,
    IsolatedBorrowRatesSchema,
)
from ccxt_pandas.wrappers.schemas.currency_schema import CurrencySchema
from ccxt_pandas.wrappers.schemas.deposit_withdraw_fees_schema import (
    DepositWithdrawFeesSchema,
)
from ccxt_pandas.wrappers.schemas.funding_history_schema import FundingHistorySchema
from ccxt_pandas.wrappers.schemas.funding_intervals_schema import FundingIntervalsSchema
from ccxt_pandas.wrappers.schemas.funding_rate_schema import FundingRateSchema
from ccxt_pandas.wrappers.schemas.funding_rate_history_schema import (
    FundingRateHistorySchema,
)
from ccxt_pandas.wrappers.schemas.greeks_schema import GreeksSchema
from ccxt_pandas.wrappers.schemas.last_prices_schema import LastPricesSchema
from ccxt_pandas.wrappers.schemas.ledger_schema import LedgerSchema
from ccxt_pandas.wrappers.schemas.leverages_schema import LeveragesSchema
from ccxt_pandas.wrappers.schemas.liquidations_schema import LiquidationsSchema
from ccxt_pandas.wrappers.schemas.long_short_ratio_schema import LongShortRatioSchema
from ccxt_pandas.wrappers.schemas.margins_balance_schema import MarginsBalanceSchema
from ccxt_pandas.wrappers.schemas.mark_prices_schema import MarkPricesSchema
from ccxt_pandas.wrappers.schemas.market_schema import MarketSchema
from ccxt_pandas.wrappers.schemas.ohlcv_schema import OHLCVSchema
from ccxt_pandas.wrappers.schemas.open_interest_history_schema import (
    OpenInterestHistorySchema,
)
from ccxt_pandas.wrappers.schemas.order_schema import OrderSchema
from ccxt_pandas.wrappers.schemas.orders_schema import OrdersSchema
from ccxt_pandas.wrappers.schemas.order_book_schema import OrderBookSchema
from ccxt_pandas.wrappers.schemas.portfolio_details_schema import PortfolioDetailsSchema
from ccxt_pandas.wrappers.schemas.portfolios_schema import PortfoliosSchema
from ccxt_pandas.wrappers.schemas.positions_schema import PositionsSchema
from ccxt_pandas.wrappers.schemas.positions_history_schema import PositionsHistorySchema
from ccxt_pandas.wrappers.schemas.tickers_schema import TickersSchema
from ccxt_pandas.wrappers.schemas.trade_schema import MyTradesSchema, TradeSchema
from ccxt_pandas.wrappers.schemas.trading_fees_schema import TradingFeesSchema
from ccxt_pandas.wrappers.schemas.transactions_schema import TransactionsSchema
from ccxt_pandas.wrappers.schemas.transfers_schema import TransfersSchema
from ccxt_pandas.wrappers.schemas.volatility_history_schema import (
    VolatilityHistorySchema,
)

__all__ = [
    "AccountsSchema",
    "AddressesSchema",
    "BaseExchangeSchema",
    "FeeFieldsMixin",
    "OrderSchema",
    "OHLCVSchema",
    "BalanceSchema",
    "MarketSchema",
    "CrossBorrowRatesSchema",
    "CurrencySchema",
    "DepositWithdrawFeesSchema",
    "OrderBookSchema",
    "TickersSchema",
    "TradeSchema",
    "BidsAsksSchema",
    "BorrowInterestSchema",
    "FundingHistorySchema",
    "FundingIntervalsSchema",
    "FundingRateSchema",
    "FundingRateHistorySchema",
    "GreeksSchema",
    "IsolatedBorrowRatesSchema",
    "LastPricesSchema",
    "LedgerSchema",
    "LeveragesSchema",
    "LiquidationsSchema",
    "LongShortRatioSchema",
    "MarginsBalanceSchema",
    "MarkPricesSchema",
    "MyTradesSchema",
    "OpenInterestHistorySchema",
    "OrdersSchema",
    "PortfolioDetailsSchema",
    "PortfoliosSchema",
    "PositionsSchema",
    "PositionsHistorySchema",
    "TradingFeesSchema",
    "TransactionsSchema",
    "TransfersSchema",
    "VolatilityHistorySchema",
]
