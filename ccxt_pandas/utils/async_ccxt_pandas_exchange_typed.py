from collections.abc import Awaitable
from decimal import Decimal
from typing import Literal, Protocol

import pandas as pd
from pandera.typing import DataFrame

from ccxt_pandas.wrappers.schemas import (
    AccountsSchema,
    AddressesSchema,
    BalanceSchema,
    BidsAsksSchema,
    BorrowInterestSchema,
    CrossBorrowRatesSchema,
    CurrencySchema,
    DepositWithdrawFeesSchema,
    FundingHistorySchema,
    FundingIntervalsSchema,
    FundingRateHistorySchema,
    FundingRateSchema,
    GreeksSchema,
    IsolatedBorrowRatesSchema,
    LastPricesSchema,
    LedgerSchema,
    LeveragesSchema,
    LiquidationsSchema,
    LongShortRatioSchema,
    MarketSchema,
    MarkPricesSchema,
    MyTradesSchema,
    OHLCVSchema,
    OpenInterestHistorySchema,
    OrderBookSchema,
    OrdersSchema,
    PositionsADLRankSchema,
    PositionsHistorySchema,
    PositionsSchema,
    TickersSchema,
    TradeSchema,
    TradingFeesSchema,
    TransactionsSchema,
    TransfersSchema,
)


class AsyncCCXTPandasExchangeTyped(Protocol):
    """A Class to add type hinting to AsyncCCXTPandasExchangeTyped"""

    def cancelAllOrders(
        self, symbol: str | list[str] = None, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.cancelAllOrders"""
        ...

    def cancelAllOrdersWs(
        self, symbol: str | list[str] = None, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.cancelAllOrdersWs"""
        ...

    def cancelOrder(
        self, id: str, symbol: str | list[str] = None, params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.cancelOrder"""
        ...

    def cancelOrderWs(
        self, id: str, symbol: str | list[str] = None, params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.cancelOrderWs"""
        ...

    def cancelOrders(
        self, ids: list[str], symbol: str | list[str] = None, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.cancelOrders"""
        ...

    def cancelOrdersForSymbols(
        self, orders: pd.DataFrame, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.cancelOrdersForSymbols"""
        ...

    def cancelOrdersWs(
        self, ids: list[str], symbol: str | list[str] = None, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.cancelOrdersWs"""
        ...

    def cancel_all_orders(
        self, symbol: str | list[str] = None, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.cancel_all_orders"""
        ...

    def cancel_all_orders_ws(
        self, symbol: str | list[str] = None, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.cancel_all_orders_ws"""
        ...

    def cancel_order(
        self, id: str, symbol: str | list[str] = None, params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.cancel_order"""
        ...

    def cancel_order_ws(
        self, id: str, symbol: str | list[str] = None, params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.cancel_order_ws"""
        ...

    def cancel_orders(
        self, ids: list[str], symbol: str | list[str] = None, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.cancel_orders"""
        ...

    def cancel_orders_for_symbols(
        self, orders: pd.DataFrame, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.cancel_orders_for_symbols"""
        ...

    def cancel_orders_ws(
        self, ids: list[str], symbol: str | list[str] = None, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.cancel_orders_ws"""
        ...

    def createOrder(
        self,
        symbol: str | list[str],
        type: Literal["limit", "market"],
        side: Literal["buy", "sell"],
        amount: float,
        price: None | str | float | int | Decimal = None,
        params={},
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.createOrder"""
        ...

    def createOrderWs(
        self,
        symbol: str | list[str],
        type: Literal["limit", "market"],
        side: Literal["buy", "sell"],
        amount: float,
        price: None | str | float | int | Decimal = None,
        params={},
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.createOrderWs"""
        ...

    def createOrders(
        self, orders: pd.DataFrame, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.createOrders"""
        ...

    def createOrdersWs(
        self, orders: pd.DataFrame, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.createOrdersWs"""
        ...

    def create_order(
        self,
        symbol: str | list[str],
        type: Literal["limit", "market"],
        side: Literal["buy", "sell"],
        amount: float,
        price: None | str | float | int | Decimal = None,
        params={},
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.create_order"""
        ...

    def create_order_ws(
        self,
        symbol: str | list[str],
        type: Literal["limit", "market"],
        side: Literal["buy", "sell"],
        amount: float,
        price: None | str | float | int | Decimal = None,
        params={},
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.create_order_ws"""
        ...

    def create_orders(
        self, orders: pd.DataFrame, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.create_orders"""
        ...

    def create_orders_ws(
        self, orders: pd.DataFrame, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.create_orders_ws"""
        ...

    def editOrder(
        self,
        id: str,
        symbol: str | list[str],
        type: Literal["limit", "market"],
        side: Literal["buy", "sell"],
        amount: None | str | float | int | Decimal = None,
        price: None | str | float | int | Decimal = None,
        params={},
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.editOrder"""
        ...

    def editOrderWs(
        self,
        id: str,
        symbol: str | list[str],
        type: Literal["limit", "market"],
        side: Literal["buy", "sell"],
        amount: None | str | float | int | Decimal = None,
        price: None | str | float | int | Decimal = None,
        params={},
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.editOrderWs"""
        ...

    def editOrders(
        self, orders: pd.DataFrame, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.editOrders"""
        ...

    def edit_order(
        self,
        id: str,
        symbol: str | list[str],
        type: Literal["limit", "market"],
        side: Literal["buy", "sell"],
        amount: None | str | float | int | Decimal = None,
        price: None | str | float | int | Decimal = None,
        params={},
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.edit_order"""
        ...

    def edit_order_ws(
        self,
        id: str,
        symbol: str | list[str],
        type: Literal["limit", "market"],
        side: Literal["buy", "sell"],
        amount: None | str | float | int | Decimal = None,
        price: None | str | float | int | Decimal = None,
        params={},
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.edit_order_ws"""
        ...

    def edit_orders(
        self, orders: pd.DataFrame, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.edit_orders"""
        ...

    def fetchADLRank(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetchADLRank"""
        ...

    def fetchAccounts(
        self, params={}
    ) -> Awaitable[DataFrame[AccountsSchema]] | list[Awaitable[DataFrame[AccountsSchema]]]:
        """Returns a DataFrame[AccountsSchema] from ccxt.fetchAccounts"""
        ...

    def fetchAllGreeks(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[DataFrame[GreeksSchema]] | list[Awaitable[DataFrame[GreeksSchema]]]:
        """Returns a DataFrame[GreeksSchema] from ccxt.fetchAllGreeks"""
        ...

    def fetchBalance(
        self, params={}
    ) -> Awaitable[DataFrame[BalanceSchema]] | list[Awaitable[DataFrame[BalanceSchema]]]:
        """Returns a DataFrame[BalanceSchema] from ccxt.fetchBalance"""
        ...

    def fetchBidsAsks(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[DataFrame[BidsAsksSchema]] | list[Awaitable[DataFrame[BidsAsksSchema]]]:
        """Returns a DataFrame[BidsAsksSchema] from ccxt.fetchBidsAsks"""
        ...

    def fetchBorrowInterest(
        self,
        code: str | list[str] = None,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> (
        Awaitable[DataFrame[BorrowInterestSchema]]
        | list[Awaitable[DataFrame[BorrowInterestSchema]]]
    ):
        """Returns a DataFrame[BorrowInterestSchema] from ccxt.fetchBorrowInterest"""
        ...

    def fetchCanceledAndClosedOrders(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[OrdersSchema]] | list[Awaitable[DataFrame[OrdersSchema]]]:
        """Returns a DataFrame[OrdersSchema] from ccxt.fetchCanceledAndClosedOrders"""
        ...

    def fetchCanceledOrders(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[OrdersSchema]] | list[Awaitable[DataFrame[OrdersSchema]]]:
        """Returns a DataFrame[OrdersSchema] from ccxt.fetchCanceledOrders"""
        ...

    def fetchClosedOrders(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[OrdersSchema]] | list[Awaitable[DataFrame[OrdersSchema]]]:
        """Returns a DataFrame[OrdersSchema] from ccxt.fetchClosedOrders"""
        ...

    def fetchConvertCurrencies(
        self, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.fetchConvertCurrencies"""
        ...

    def fetchConvertTradeHistory(
        self,
        code: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.fetchConvertTradeHistory"""
        ...

    def fetchCrossBorrowRate(
        self, code: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetchCrossBorrowRate"""
        ...

    def fetchCrossBorrowRates(
        self, params={}
    ) -> (
        Awaitable[DataFrame[CrossBorrowRatesSchema]]
        | list[Awaitable[DataFrame[CrossBorrowRatesSchema]]]
    ):
        """Returns a DataFrame[CrossBorrowRatesSchema] from ccxt.fetchCrossBorrowRates"""
        ...

    def fetchCurrencies(
        self, params={}
    ) -> Awaitable[DataFrame[CurrencySchema]] | list[Awaitable[DataFrame[CurrencySchema]]]:
        """Returns a DataFrame[CurrencySchema] from ccxt.fetchCurrencies"""
        ...

    def fetchDepositAddresses(
        self, codes: list[str] | None = None, params={}
    ) -> Awaitable[DataFrame[AddressesSchema]] | list[Awaitable[DataFrame[AddressesSchema]]]:
        """Returns a DataFrame[AddressesSchema] from ccxt.fetchDepositAddresses"""
        ...

    def fetchDepositWithdrawFee(
        self, code: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetchDepositWithdrawFee"""
        ...

    def fetchDepositWithdrawFees(
        self, codes: list[str] | None = None, params={}
    ) -> (
        Awaitable[DataFrame[DepositWithdrawFeesSchema]]
        | list[Awaitable[DataFrame[DepositWithdrawFeesSchema]]]
    ):
        """Returns a DataFrame[DepositWithdrawFeesSchema] from ccxt.fetchDepositWithdrawFees"""
        ...

    def fetchDeposits(
        self,
        code: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[TransactionsSchema]] | list[Awaitable[DataFrame[TransactionsSchema]]]:
        """Returns a DataFrame[TransactionsSchema] from ccxt.fetchDeposits"""
        ...

    def fetchDepositsWithdrawals(
        self,
        code: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[TransactionsSchema]] | list[Awaitable[DataFrame[TransactionsSchema]]]:
        """Returns a DataFrame[TransactionsSchema] from ccxt.fetchDepositsWithdrawals"""
        ...

    def fetchFundingHistory(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> (
        Awaitable[DataFrame[FundingHistorySchema]]
        | list[Awaitable[DataFrame[FundingHistorySchema]]]
    ):
        """Returns a DataFrame[FundingHistorySchema] from ccxt.fetchFundingHistory"""
        ...

    def fetchFundingInterval(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetchFundingInterval"""
        ...

    def fetchFundingIntervals(
        self, symbols: list[str] | None = None, params={}
    ) -> (
        Awaitable[DataFrame[FundingIntervalsSchema]]
        | list[Awaitable[DataFrame[FundingIntervalsSchema]]]
    ):
        """Returns a DataFrame[FundingIntervalsSchema] from ccxt.fetchFundingIntervals"""
        ...

    def fetchFundingRate(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetchFundingRate"""
        ...

    def fetchFundingRateHistory(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> (
        Awaitable[DataFrame[FundingRateHistorySchema]]
        | list[Awaitable[DataFrame[FundingRateHistorySchema]]]
    ):
        """Returns a DataFrame[FundingRateHistorySchema] from ccxt.fetchFundingRateHistory"""
        ...

    def fetchFundingRates(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[DataFrame[FundingRateSchema]] | list[Awaitable[DataFrame[FundingRateSchema]]]:
        """Returns a DataFrame[FundingRateSchema] from ccxt.fetchFundingRates"""
        ...

    def fetchGreeks(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetchGreeks"""
        ...

    def fetchIsolatedBorrowRate(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetchIsolatedBorrowRate"""
        ...

    def fetchIsolatedBorrowRates(
        self, params={}
    ) -> (
        Awaitable[DataFrame[IsolatedBorrowRatesSchema]]
        | list[Awaitable[DataFrame[IsolatedBorrowRatesSchema]]]
    ):
        """Returns a DataFrame[IsolatedBorrowRatesSchema] from ccxt.fetchIsolatedBorrowRates"""
        ...

    def fetchL3OrderBook(
        self, symbol: str | list[str], limit: int | None = None, params={}
    ) -> Awaitable[DataFrame[OrderBookSchema]] | list[Awaitable[DataFrame[OrderBookSchema]]]:
        """Returns a DataFrame[OrderBookSchema] from ccxt.fetchL3OrderBook"""
        ...

    def fetchLastPrices(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[DataFrame[LastPricesSchema]] | list[Awaitable[DataFrame[LastPricesSchema]]]:
        """Returns a DataFrame[LastPricesSchema] from ccxt.fetchLastPrices"""
        ...

    def fetchLedger(
        self,
        code: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[LedgerSchema]] | list[Awaitable[DataFrame[LedgerSchema]]]:
        """Returns a DataFrame[LedgerSchema] from ccxt.fetchLedger"""
        ...

    def fetchLeverageTiers(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.fetchLeverageTiers"""
        ...

    def fetchLeverages(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[DataFrame[LeveragesSchema]] | list[Awaitable[DataFrame[LeveragesSchema]]]:
        """Returns a DataFrame[LeveragesSchema] from ccxt.fetchLeverages"""
        ...

    def fetchLiquidations(
        self,
        symbol: str | list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[LiquidationsSchema]] | list[Awaitable[DataFrame[LiquidationsSchema]]]:
        """Returns a DataFrame[LiquidationsSchema] from ccxt.fetchLiquidations"""
        ...

    def fetchLongShortRatioHistory(
        self,
        symbol: str | list[str] = None,
        timeframe: str | None = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> (
        Awaitable[DataFrame[LongShortRatioSchema]]
        | list[Awaitable[DataFrame[LongShortRatioSchema]]]
    ):
        """Returns a DataFrame[LongShortRatioSchema] from ccxt.fetchLongShortRatioHistory"""
        ...

    def fetchMarginAdjustmentHistory(
        self,
        symbol: str | list[str] = None,
        type: str | None = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: None | str | float | int | Decimal = None,
        params={},
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.fetchMarginAdjustmentHistory"""
        ...

    def fetchMarginModes(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.fetchMarginModes"""
        ...

    def fetchMarkPrice(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetchMarkPrice"""
        ...

    def fetchMarkPrices(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[DataFrame[MarkPricesSchema]] | list[Awaitable[DataFrame[MarkPricesSchema]]]:
        """Returns a DataFrame[MarkPricesSchema] from ccxt.fetchMarkPrices"""
        ...

    def fetchMarkets(
        self, params={}
    ) -> Awaitable[DataFrame[MarketSchema]] | list[Awaitable[DataFrame[MarketSchema]]]:
        """Returns a DataFrame[MarketSchema] from ccxt.fetchMarkets"""
        ...

    def fetchMyLiquidations(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[LiquidationsSchema]] | list[Awaitable[DataFrame[LiquidationsSchema]]]:
        """Returns a DataFrame[LiquidationsSchema] from ccxt.fetchMyLiquidations"""
        ...

    def fetchMyTrades(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[MyTradesSchema]] | list[Awaitable[DataFrame[MyTradesSchema]]]:
        """Returns a DataFrame[MyTradesSchema] from ccxt.fetchMyTrades"""
        ...

    def fetchOHLCV(
        self,
        symbol: str | list[str],
        timeframe: str = "1m",
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.fetchOHLCV"""
        ...

    def fetchOpenInterest(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetchOpenInterest"""
        ...

    def fetchOpenInterestHistory(
        self,
        symbol: str | list[str],
        timeframe: str = "1h",
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> (
        Awaitable[DataFrame[OpenInterestHistorySchema]]
        | list[Awaitable[DataFrame[OpenInterestHistorySchema]]]
    ):
        """Returns a DataFrame[OpenInterestHistorySchema] from ccxt.fetchOpenInterestHistory"""
        ...

    def fetchOpenInterests(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.fetchOpenInterests"""
        ...

    def fetchOpenOrders(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[OrdersSchema]] | list[Awaitable[DataFrame[OrdersSchema]]]:
        """Returns a DataFrame[OrdersSchema] from ccxt.fetchOpenOrders"""
        ...

    def fetchOption(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetchOption"""
        ...

    def fetchOptionChain(
        self, code: str | list[str], params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.fetchOptionChain"""
        ...

    def fetchOrder(
        self, id: str, symbol: str | list[str] = None, params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetchOrder"""
        ...

    def fetchOrderBook(
        self, symbol: str | list[str], limit: int | None = None, params={}
    ) -> Awaitable[DataFrame[OrderBookSchema]] | list[Awaitable[DataFrame[OrderBookSchema]]]:
        """Returns a DataFrame[OrderBookSchema] from ccxt.fetchOrderBook"""
        ...

    def fetchOrderBooks(
        self, symbols: list[str] | None = None, limit: int | None = None, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.fetchOrderBooks"""
        ...

    def fetchOrderTrades(
        self,
        id: str,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.fetchOrderTrades"""
        ...

    def fetchOrders(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[OrdersSchema]] | list[Awaitable[DataFrame[OrdersSchema]]]:
        """Returns a DataFrame[OrdersSchema] from ccxt.fetchOrders"""
        ...

    def fetchOrdersWs(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[OrdersSchema]] | list[Awaitable[DataFrame[OrdersSchema]]]:
        """Returns a DataFrame[OrdersSchema] from ccxt.fetchOrdersWs"""
        ...

    def fetchPosition(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetchPosition"""
        ...

    def fetchPositionADLRank(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetchPositionADLRank"""
        ...

    def fetchPositionHistory(
        self,
        symbol: str | list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> (
        Awaitable[DataFrame[PositionsHistorySchema]]
        | list[Awaitable[DataFrame[PositionsHistorySchema]]]
    ):
        """Returns a DataFrame[PositionsHistorySchema] from ccxt.fetchPositionHistory"""
        ...

    def fetchPositions(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[DataFrame[PositionsSchema]] | list[Awaitable[DataFrame[PositionsSchema]]]:
        """Returns a DataFrame[PositionsSchema] from ccxt.fetchPositions"""
        ...

    def fetchPositionsADLRank(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.fetchPositionsADLRank"""
        ...

    def fetchPositionsHistory(
        self,
        symbols: list[str] | None = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        limit: int | None = None,
        params={},
    ) -> (
        Awaitable[DataFrame[PositionsHistorySchema]]
        | list[Awaitable[DataFrame[PositionsHistorySchema]]]
    ):
        """Returns a DataFrame[PositionsHistorySchema] from ccxt.fetchPositionsHistory"""
        ...

    def fetchPositionsRisk(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.fetchPositionsRisk"""
        ...

    def fetchStatus(self, params={}) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetchStatus"""
        ...

    def fetchTicker(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetchTicker"""
        ...

    def fetchTickers(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[DataFrame[TickersSchema]] | list[Awaitable[DataFrame[TickersSchema]]]:
        """Returns a DataFrame[TickersSchema] from ccxt.fetchTickers"""
        ...

    def fetchTrades(
        self,
        symbol: str | list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[TradeSchema]] | list[Awaitable[DataFrame[TradeSchema]]]:
        """Returns a DataFrame[TradeSchema] from ccxt.fetchTrades"""
        ...

    def fetchTradingFee(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetchTradingFee"""
        ...

    def fetchTradingFees(
        self, params={}
    ) -> Awaitable[DataFrame[TradingFeesSchema]] | list[Awaitable[DataFrame[TradingFeesSchema]]]:
        """Returns a DataFrame[TradingFeesSchema] from ccxt.fetchTradingFees"""
        ...

    def fetchTransactionFees(
        self, codes: list[str] | None = None, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.fetchTransactionFees"""
        ...

    def fetchTransfers(
        self,
        code: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[TransfersSchema]] | list[Awaitable[DataFrame[TransfersSchema]]]:
        """Returns a DataFrame[TransfersSchema] from ccxt.fetchTransfers"""
        ...

    def fetchWithdrawals(
        self,
        code: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[TransactionsSchema]] | list[Awaitable[DataFrame[TransactionsSchema]]]:
        """Returns a DataFrame[TransactionsSchema] from ccxt.fetchWithdrawals"""
        ...

    def fetch_accounts(
        self, params={}
    ) -> Awaitable[DataFrame[AccountsSchema]] | list[Awaitable[DataFrame[AccountsSchema]]]:
        """Returns a DataFrame[AccountsSchema] from ccxt.fetch_accounts"""
        ...

    def fetch_adl_rank(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetch_adl_rank"""
        ...

    def fetch_all_greeks(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[DataFrame[GreeksSchema]] | list[Awaitable[DataFrame[GreeksSchema]]]:
        """Returns a DataFrame[GreeksSchema] from ccxt.fetch_all_greeks"""
        ...

    def fetch_balance(
        self, params={}
    ) -> Awaitable[DataFrame[BalanceSchema]] | list[Awaitable[DataFrame[BalanceSchema]]]:
        """Returns a DataFrame[BalanceSchema] from ccxt.fetch_balance"""
        ...

    def fetch_bids_asks(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[DataFrame[BidsAsksSchema]] | list[Awaitable[DataFrame[BidsAsksSchema]]]:
        """Returns a DataFrame[BidsAsksSchema] from ccxt.fetch_bids_asks"""
        ...

    def fetch_borrow_interest(
        self,
        code: str | list[str] = None,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> (
        Awaitable[DataFrame[BorrowInterestSchema]]
        | list[Awaitable[DataFrame[BorrowInterestSchema]]]
    ):
        """Returns a DataFrame[BorrowInterestSchema] from ccxt.fetch_borrow_interest"""
        ...

    def fetch_canceled_and_closed_orders(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[OrdersSchema]] | list[Awaitable[DataFrame[OrdersSchema]]]:
        """Returns a DataFrame[OrdersSchema] from ccxt.fetch_canceled_and_closed_orders"""
        ...

    def fetch_canceled_orders(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[OrdersSchema]] | list[Awaitable[DataFrame[OrdersSchema]]]:
        """Returns a DataFrame[OrdersSchema] from ccxt.fetch_canceled_orders"""
        ...

    def fetch_closed_orders(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[OrdersSchema]] | list[Awaitable[DataFrame[OrdersSchema]]]:
        """Returns a DataFrame[OrdersSchema] from ccxt.fetch_closed_orders"""
        ...

    def fetch_convert_currencies(
        self, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.fetch_convert_currencies"""
        ...

    def fetch_convert_trade_history(
        self,
        code: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.fetch_convert_trade_history"""
        ...

    def fetch_cross_borrow_rate(
        self, code: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetch_cross_borrow_rate"""
        ...

    def fetch_cross_borrow_rates(
        self, params={}
    ) -> (
        Awaitable[DataFrame[CrossBorrowRatesSchema]]
        | list[Awaitable[DataFrame[CrossBorrowRatesSchema]]]
    ):
        """Returns a DataFrame[CrossBorrowRatesSchema] from ccxt.fetch_cross_borrow_rates"""
        ...

    def fetch_currencies(
        self, params={}
    ) -> Awaitable[DataFrame[CurrencySchema]] | list[Awaitable[DataFrame[CurrencySchema]]]:
        """Returns a DataFrame[CurrencySchema] from ccxt.fetch_currencies"""
        ...

    def fetch_deposit_addresses(
        self, codes: list[str] | None = None, params={}
    ) -> Awaitable[DataFrame[AddressesSchema]] | list[Awaitable[DataFrame[AddressesSchema]]]:
        """Returns a DataFrame[AddressesSchema] from ccxt.fetch_deposit_addresses"""
        ...

    def fetch_deposit_withdraw_fee(
        self, code: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetch_deposit_withdraw_fee"""
        ...

    def fetch_deposit_withdraw_fees(
        self, codes: list[str] | None = None, params={}
    ) -> (
        Awaitable[DataFrame[DepositWithdrawFeesSchema]]
        | list[Awaitable[DataFrame[DepositWithdrawFeesSchema]]]
    ):
        """Returns a DataFrame[DepositWithdrawFeesSchema] from ccxt.fetch_deposit_withdraw_fees"""
        ...

    def fetch_deposits(
        self,
        code: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[TransactionsSchema]] | list[Awaitable[DataFrame[TransactionsSchema]]]:
        """Returns a DataFrame[TransactionsSchema] from ccxt.fetch_deposits"""
        ...

    def fetch_deposits_withdrawals(
        self,
        code: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[TransactionsSchema]] | list[Awaitable[DataFrame[TransactionsSchema]]]:
        """Returns a DataFrame[TransactionsSchema] from ccxt.fetch_deposits_withdrawals"""
        ...

    def fetch_funding_history(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> (
        Awaitable[DataFrame[FundingHistorySchema]]
        | list[Awaitable[DataFrame[FundingHistorySchema]]]
    ):
        """Returns a DataFrame[FundingHistorySchema] from ccxt.fetch_funding_history"""
        ...

    def fetch_funding_interval(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetch_funding_interval"""
        ...

    def fetch_funding_intervals(
        self, symbols: list[str] | None = None, params={}
    ) -> (
        Awaitable[DataFrame[FundingIntervalsSchema]]
        | list[Awaitable[DataFrame[FundingIntervalsSchema]]]
    ):
        """Returns a DataFrame[FundingIntervalsSchema] from ccxt.fetch_funding_intervals"""
        ...

    def fetch_funding_rate(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetch_funding_rate"""
        ...

    def fetch_funding_rate_history(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> (
        Awaitable[DataFrame[FundingRateHistorySchema]]
        | list[Awaitable[DataFrame[FundingRateHistorySchema]]]
    ):
        """Returns a DataFrame[FundingRateHistorySchema] from ccxt.fetch_funding_rate_history"""
        ...

    def fetch_funding_rates(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[DataFrame[FundingRateSchema]] | list[Awaitable[DataFrame[FundingRateSchema]]]:
        """Returns a DataFrame[FundingRateSchema] from ccxt.fetch_funding_rates"""
        ...

    def fetch_greeks(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetch_greeks"""
        ...

    def fetch_isolated_borrow_rate(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetch_isolated_borrow_rate"""
        ...

    def fetch_isolated_borrow_rates(
        self, params={}
    ) -> (
        Awaitable[DataFrame[IsolatedBorrowRatesSchema]]
        | list[Awaitable[DataFrame[IsolatedBorrowRatesSchema]]]
    ):
        """Returns a DataFrame[IsolatedBorrowRatesSchema] from ccxt.fetch_isolated_borrow_rates"""
        ...

    def fetch_l3_order_book(
        self, symbol: str | list[str], limit: int | None = None, params={}
    ) -> Awaitable[DataFrame[OrderBookSchema]] | list[Awaitable[DataFrame[OrderBookSchema]]]:
        """Returns a DataFrame[OrderBookSchema] from ccxt.fetch_l3_order_book"""
        ...

    def fetch_last_prices(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[DataFrame[LastPricesSchema]] | list[Awaitable[DataFrame[LastPricesSchema]]]:
        """Returns a DataFrame[LastPricesSchema] from ccxt.fetch_last_prices"""
        ...

    def fetch_ledger(
        self,
        code: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[LedgerSchema]] | list[Awaitable[DataFrame[LedgerSchema]]]:
        """Returns a DataFrame[LedgerSchema] from ccxt.fetch_ledger"""
        ...

    def fetch_leverage_tiers(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.fetch_leverage_tiers"""
        ...

    def fetch_leverages(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[DataFrame[LeveragesSchema]] | list[Awaitable[DataFrame[LeveragesSchema]]]:
        """Returns a DataFrame[LeveragesSchema] from ccxt.fetch_leverages"""
        ...

    def fetch_liquidations(
        self,
        symbol: str | list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[LiquidationsSchema]] | list[Awaitable[DataFrame[LiquidationsSchema]]]:
        """Returns a DataFrame[LiquidationsSchema] from ccxt.fetch_liquidations"""
        ...

    def fetch_long_short_ratio_history(
        self,
        symbol: str | list[str] = None,
        timeframe: str | None = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> (
        Awaitable[DataFrame[LongShortRatioSchema]]
        | list[Awaitable[DataFrame[LongShortRatioSchema]]]
    ):
        """Returns a DataFrame[LongShortRatioSchema] from ccxt.fetch_long_short_ratio_history"""
        ...

    def fetch_margin_adjustment_history(
        self,
        symbol: str | list[str] = None,
        type: str | None = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: None | str | float | int | Decimal = None,
        params={},
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.fetch_margin_adjustment_history"""
        ...

    def fetch_margin_modes(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.fetch_margin_modes"""
        ...

    def fetch_mark_price(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetch_mark_price"""
        ...

    def fetch_mark_prices(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[DataFrame[MarkPricesSchema]] | list[Awaitable[DataFrame[MarkPricesSchema]]]:
        """Returns a DataFrame[MarkPricesSchema] from ccxt.fetch_mark_prices"""
        ...

    def fetch_markets(
        self, params={}
    ) -> Awaitable[DataFrame[MarketSchema]] | list[Awaitable[DataFrame[MarketSchema]]]:
        """Returns a DataFrame[MarketSchema] from ccxt.fetch_markets"""
        ...

    def fetch_my_liquidations(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[LiquidationsSchema]] | list[Awaitable[DataFrame[LiquidationsSchema]]]:
        """Returns a DataFrame[LiquidationsSchema] from ccxt.fetch_my_liquidations"""
        ...

    def fetch_my_trades(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[MyTradesSchema]] | list[Awaitable[DataFrame[MyTradesSchema]]]:
        """Returns a DataFrame[MyTradesSchema] from ccxt.fetch_my_trades"""
        ...

    def fetch_ohlcv(
        self,
        symbol: str | list[str],
        timeframe: str = "1m",
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[OHLCVSchema]] | list[Awaitable[DataFrame[OHLCVSchema]]]:
        """Returns a DataFrame[OHLCVSchema] from ccxt.fetch_ohlcv"""
        ...

    def fetch_open_interest(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetch_open_interest"""
        ...

    def fetch_open_interest_history(
        self,
        symbol: str | list[str],
        timeframe: str = "1h",
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> (
        Awaitable[DataFrame[OpenInterestHistorySchema]]
        | list[Awaitable[DataFrame[OpenInterestHistorySchema]]]
    ):
        """Returns a DataFrame[OpenInterestHistorySchema] from ccxt.fetch_open_interest_history"""
        ...

    def fetch_open_interests(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.fetch_open_interests"""
        ...

    def fetch_open_orders(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[OrdersSchema]] | list[Awaitable[DataFrame[OrdersSchema]]]:
        """Returns a DataFrame[OrdersSchema] from ccxt.fetch_open_orders"""
        ...

    def fetch_option(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetch_option"""
        ...

    def fetch_option_chain(
        self, code: str | list[str], params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.fetch_option_chain"""
        ...

    def fetch_order(
        self, id: str, symbol: str | list[str] = None, params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetch_order"""
        ...

    def fetch_order_book(
        self, symbol: str | list[str], limit: int | None = None, params={}
    ) -> Awaitable[DataFrame[OrderBookSchema]] | list[Awaitable[DataFrame[OrderBookSchema]]]:
        """Returns a DataFrame[OrderBookSchema] from ccxt.fetch_order_book"""
        ...

    def fetch_order_books(
        self, symbols: list[str] | None = None, limit: int | None = None, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.fetch_order_books"""
        ...

    def fetch_order_trades(
        self,
        id: str,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.fetch_order_trades"""
        ...

    def fetch_orders(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[OrdersSchema]] | list[Awaitable[DataFrame[OrdersSchema]]]:
        """Returns a DataFrame[OrdersSchema] from ccxt.fetch_orders"""
        ...

    def fetch_orders_ws(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[OrdersSchema]] | list[Awaitable[DataFrame[OrdersSchema]]]:
        """Returns a DataFrame[OrdersSchema] from ccxt.fetch_orders_ws"""
        ...

    def fetch_position(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetch_position"""
        ...

    def fetch_position_adl_rank(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetch_position_adl_rank"""
        ...

    def fetch_position_history(
        self,
        symbol: str | list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> (
        Awaitable[DataFrame[PositionsHistorySchema]]
        | list[Awaitable[DataFrame[PositionsHistorySchema]]]
    ):
        """Returns a DataFrame[PositionsHistorySchema] from ccxt.fetch_position_history"""
        ...

    def fetch_positions(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[DataFrame[PositionsSchema]] | list[Awaitable[DataFrame[PositionsSchema]]]:
        """Returns a DataFrame[PositionsSchema] from ccxt.fetch_positions"""
        ...

    def fetch_positions_adl_rank(
        self, symbols: list[str] | None = None, params={}
    ) -> (
        Awaitable[DataFrame[PositionsADLRankSchema]]
        | list[Awaitable[DataFrame[PositionsADLRankSchema]]]
    ):
        """Returns a DataFrame[PositionsADLRankSchema] from ccxt.fetch_positions_adl_rank"""
        ...

    def fetch_positions_history(
        self,
        symbols: list[str] | None = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        limit: int | None = None,
        params={},
    ) -> (
        Awaitable[DataFrame[PositionsHistorySchema]]
        | list[Awaitable[DataFrame[PositionsHistorySchema]]]
    ):
        """Returns a DataFrame[PositionsHistorySchema] from ccxt.fetch_positions_history"""
        ...

    def fetch_positions_risk(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.fetch_positions_risk"""
        ...

    def fetch_status(self, params={}) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetch_status"""
        ...

    def fetch_ticker(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetch_ticker"""
        ...

    def fetch_tickers(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[DataFrame[TickersSchema]] | list[Awaitable[DataFrame[TickersSchema]]]:
        """Returns a DataFrame[TickersSchema] from ccxt.fetch_tickers"""
        ...

    def fetch_trades(
        self,
        symbol: str | list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[TradeSchema]] | list[Awaitable[DataFrame[TradeSchema]]]:
        """Returns a DataFrame[TradeSchema] from ccxt.fetch_trades"""
        ...

    def fetch_trading_fee(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.fetch_trading_fee"""
        ...

    def fetch_trading_fees(
        self, params={}
    ) -> Awaitable[DataFrame[TradingFeesSchema]] | list[Awaitable[DataFrame[TradingFeesSchema]]]:
        """Returns a DataFrame[TradingFeesSchema] from ccxt.fetch_trading_fees"""
        ...

    def fetch_transaction_fees(
        self, codes: list[str] | None = None, params={}
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.fetch_transaction_fees"""
        ...

    def fetch_transfers(
        self,
        code: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[TransfersSchema]] | list[Awaitable[DataFrame[TransfersSchema]]]:
        """Returns a DataFrame[TransfersSchema] from ccxt.fetch_transfers"""
        ...

    def fetch_withdrawals(
        self,
        code: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[TransactionsSchema]] | list[Awaitable[DataFrame[TransactionsSchema]]]:
        """Returns a DataFrame[TransactionsSchema] from ccxt.fetch_withdrawals"""
        ...

    def loadMarkets(
        self, reload=False, params={}
    ) -> Awaitable[DataFrame[MarketSchema]] | list[Awaitable[DataFrame[MarketSchema]]]:
        """Returns a DataFrame[MarketSchema] from ccxt.loadMarkets"""
        ...

    def load_markets(
        self, reload=False, params={}
    ) -> Awaitable[DataFrame[MarketSchema]] | list[Awaitable[DataFrame[MarketSchema]]]:
        """Returns a DataFrame[MarketSchema] from ccxt.load_markets"""
        ...

    def watchBalance(
        self, params={}
    ) -> Awaitable[DataFrame[BalanceSchema]] | list[Awaitable[DataFrame[BalanceSchema]]]:
        """Returns a DataFrame[BalanceSchema] from ccxt.watchBalance"""
        ...

    def watchBidsAsks(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[DataFrame[BidsAsksSchema]] | list[Awaitable[DataFrame[BidsAsksSchema]]]:
        """Returns a DataFrame[BidsAsksSchema] from ccxt.watchBidsAsks"""
        ...

    def watchFundingRate(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.watchFundingRate"""
        ...

    def watchFundingRates(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[DataFrame[FundingRateSchema]] | list[Awaitable[DataFrame[FundingRateSchema]]]:
        """Returns a DataFrame[FundingRateSchema] from ccxt.watchFundingRates"""
        ...

    def watchLiquidations(
        self,
        symbol: str | list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[LiquidationsSchema]] | list[Awaitable[DataFrame[LiquidationsSchema]]]:
        """Returns a DataFrame[LiquidationsSchema] from ccxt.watchLiquidations"""
        ...

    def watchLiquidationsForSymbols(
        self,
        symbols: list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[LiquidationsSchema]] | list[Awaitable[DataFrame[LiquidationsSchema]]]:
        """Returns a DataFrame[LiquidationsSchema] from ccxt.watchLiquidationsForSymbols"""
        ...

    def watchMarkPrice(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.watchMarkPrice"""
        ...

    def watchMarkPrices(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[DataFrame[MarkPricesSchema]] | list[Awaitable[DataFrame[MarkPricesSchema]]]:
        """Returns a DataFrame[MarkPricesSchema] from ccxt.watchMarkPrices"""
        ...

    def watchMyLiquidations(
        self,
        symbol: str | list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[LiquidationsSchema]] | list[Awaitable[DataFrame[LiquidationsSchema]]]:
        """Returns a DataFrame[LiquidationsSchema] from ccxt.watchMyLiquidations"""
        ...

    def watchMyLiquidationsForSymbols(
        self,
        symbols: list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[LiquidationsSchema]] | list[Awaitable[DataFrame[LiquidationsSchema]]]:
        """Returns a DataFrame[LiquidationsSchema] from ccxt.watchMyLiquidationsForSymbols"""
        ...

    def watchMyTrades(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[MyTradesSchema]] | list[Awaitable[DataFrame[MyTradesSchema]]]:
        """Returns a DataFrame[MyTradesSchema] from ccxt.watchMyTrades"""
        ...

    def watchMyTradesForSymbols(
        self,
        symbols: list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[MyTradesSchema]] | list[Awaitable[DataFrame[MyTradesSchema]]]:
        """Returns a DataFrame[MyTradesSchema] from ccxt.watchMyTradesForSymbols"""
        ...

    def watchOHLCV(
        self,
        symbol: str | list[str],
        timeframe: str = "1m",
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.watchOHLCV"""
        ...

    def watchOHLCVForSymbols(
        self,
        symbolsAndTimeframes: list[list[str]],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        limit: int | None = None,
        params={},
    ) -> Awaitable[pd.DataFrame] | list[Awaitable[pd.DataFrame]]:
        """Returns a pd.DataFrame from ccxt.watchOHLCVForSymbols"""
        ...

    def watchOrderBook(
        self, symbol: str | list[str], limit: int | None = None, params={}
    ) -> Awaitable[DataFrame[OrderBookSchema]] | list[Awaitable[DataFrame[OrderBookSchema]]]:
        """Returns a DataFrame[OrderBookSchema] from ccxt.watchOrderBook"""
        ...

    def watchOrderBookForSymbols(
        self, symbols: list[str], limit: int | None = None, params={}
    ) -> Awaitable[DataFrame[OrderBookSchema]] | list[Awaitable[DataFrame[OrderBookSchema]]]:
        """Returns a DataFrame[OrderBookSchema] from ccxt.watchOrderBookForSymbols"""
        ...

    def watchOrders(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[OrdersSchema]] | list[Awaitable[DataFrame[OrdersSchema]]]:
        """Returns a DataFrame[OrdersSchema] from ccxt.watchOrders"""
        ...

    def watchOrdersForSymbols(
        self,
        symbols: list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[OrdersSchema]] | list[Awaitable[DataFrame[OrdersSchema]]]:
        """Returns a DataFrame[OrdersSchema] from ccxt.watchOrdersForSymbols"""
        ...

    def watchPosition(
        self, symbol: str | list[str] = None, params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.watchPosition"""
        ...

    def watchPositions(
        self,
        symbols: list[str] | None = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[PositionsSchema]] | list[Awaitable[DataFrame[PositionsSchema]]]:
        """Returns a DataFrame[PositionsSchema] from ccxt.watchPositions"""
        ...

    def watchTicker(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.watchTicker"""
        ...

    def watchTickers(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[DataFrame[TickersSchema]] | list[Awaitable[DataFrame[TickersSchema]]]:
        """Returns a DataFrame[TickersSchema] from ccxt.watchTickers"""
        ...

    def watchTrades(
        self,
        symbol: str | list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[TradeSchema]] | list[Awaitable[DataFrame[TradeSchema]]]:
        """Returns a DataFrame[TradeSchema] from ccxt.watchTrades"""
        ...

    def watchTradesForSymbols(
        self,
        symbols: list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[TradeSchema]] | list[Awaitable[DataFrame[TradeSchema]]]:
        """Returns a DataFrame[TradeSchema] from ccxt.watchTradesForSymbols"""
        ...

    def watch_balance(
        self, params={}
    ) -> Awaitable[DataFrame[BalanceSchema]] | list[Awaitable[DataFrame[BalanceSchema]]]:
        """Returns a DataFrame[BalanceSchema] from ccxt.watch_balance"""
        ...

    def watch_bids_asks(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[DataFrame[BidsAsksSchema]] | list[Awaitable[DataFrame[BidsAsksSchema]]]:
        """Returns a DataFrame[BidsAsksSchema] from ccxt.watch_bids_asks"""
        ...

    def watch_funding_rate(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.watch_funding_rate"""
        ...

    def watch_funding_rates(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[DataFrame[FundingRateSchema]] | list[Awaitable[DataFrame[FundingRateSchema]]]:
        """Returns a DataFrame[FundingRateSchema] from ccxt.watch_funding_rates"""
        ...

    def watch_liquidations(
        self,
        symbol: str | list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[LiquidationsSchema]] | list[Awaitable[DataFrame[LiquidationsSchema]]]:
        """Returns a DataFrame[LiquidationsSchema] from ccxt.watch_liquidations"""
        ...

    def watch_liquidations_for_symbols(
        self,
        symbols: list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[LiquidationsSchema]] | list[Awaitable[DataFrame[LiquidationsSchema]]]:
        """Returns a DataFrame[LiquidationsSchema] from ccxt.watch_liquidations_for_symbols"""
        ...

    def watch_mark_price(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.watch_mark_price"""
        ...

    def watch_mark_prices(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[DataFrame[MarkPricesSchema]] | list[Awaitable[DataFrame[MarkPricesSchema]]]:
        """Returns a DataFrame[MarkPricesSchema] from ccxt.watch_mark_prices"""
        ...

    def watch_my_liquidations(
        self,
        symbol: str | list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[LiquidationsSchema]] | list[Awaitable[DataFrame[LiquidationsSchema]]]:
        """Returns a DataFrame[LiquidationsSchema] from ccxt.watch_my_liquidations"""
        ...

    def watch_my_liquidations_for_symbols(
        self,
        symbols: list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[LiquidationsSchema]] | list[Awaitable[DataFrame[LiquidationsSchema]]]:
        """Returns a DataFrame[LiquidationsSchema] from ccxt.watch_my_liquidations_for_symbols"""
        ...

    def watch_my_trades(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[MyTradesSchema]] | list[Awaitable[DataFrame[MyTradesSchema]]]:
        """Returns a DataFrame[MyTradesSchema] from ccxt.watch_my_trades"""
        ...

    def watch_my_trades_for_symbols(
        self,
        symbols: list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[MyTradesSchema]] | list[Awaitable[DataFrame[MyTradesSchema]]]:
        """Returns a DataFrame[MyTradesSchema] from ccxt.watch_my_trades_for_symbols"""
        ...

    def watch_ohlcv(
        self,
        symbol: str | list[str],
        timeframe: str = "1m",
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[OHLCVSchema]] | list[Awaitable[DataFrame[OHLCVSchema]]]:
        """Returns a DataFrame[OHLCVSchema] from ccxt.watch_ohlcv"""
        ...

    def watch_ohlcv_for_symbols(
        self,
        symbolsAndTimeframes: list[list[str]],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[OHLCVSchema]] | list[Awaitable[DataFrame[OHLCVSchema]]]:
        """Returns a DataFrame[OHLCVSchema] from ccxt.watch_ohlcv_for_symbols"""
        ...

    def watch_order_book(
        self, symbol: str | list[str], limit: int | None = None, params={}
    ) -> Awaitable[DataFrame[OrderBookSchema]] | list[Awaitable[DataFrame[OrderBookSchema]]]:
        """Returns a DataFrame[OrderBookSchema] from ccxt.watch_order_book"""
        ...

    def watch_order_book_for_symbols(
        self, symbols: list[str], limit: int | None = None, params={}
    ) -> Awaitable[DataFrame[OrderBookSchema]] | list[Awaitable[DataFrame[OrderBookSchema]]]:
        """Returns a DataFrame[OrderBookSchema] from ccxt.watch_order_book_for_symbols"""
        ...

    def watch_orders(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[OrdersSchema]] | list[Awaitable[DataFrame[OrdersSchema]]]:
        """Returns a DataFrame[OrdersSchema] from ccxt.watch_orders"""
        ...

    def watch_orders_for_symbols(
        self,
        symbols: list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[OrdersSchema]] | list[Awaitable[DataFrame[OrdersSchema]]]:
        """Returns a DataFrame[OrdersSchema] from ccxt.watch_orders_for_symbols"""
        ...

    def watch_position(
        self, symbol: str | list[str] = None, params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.watch_position"""
        ...

    def watch_positions(
        self,
        symbols: list[str] | None = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[PositionsSchema]] | list[Awaitable[DataFrame[PositionsSchema]]]:
        """Returns a DataFrame[PositionsSchema] from ccxt.watch_positions"""
        ...

    def watch_ticker(
        self, symbol: str | list[str], params={}
    ) -> Awaitable[dict] | list[Awaitable[dict]]:
        """Returns a dict from ccxt.watch_ticker"""
        ...

    def watch_tickers(
        self, symbols: list[str] | None = None, params={}
    ) -> Awaitable[DataFrame[TickersSchema]] | list[Awaitable[DataFrame[TickersSchema]]]:
        """Returns a DataFrame[TickersSchema] from ccxt.watch_tickers"""
        ...

    def watch_trades(
        self,
        symbol: str | list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[TradeSchema]] | list[Awaitable[DataFrame[TradeSchema]]]:
        """Returns a DataFrame[TradeSchema] from ccxt.watch_trades"""
        ...

    def watch_trades_for_symbols(
        self,
        symbols: list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        limit: int | None = None,
        params={},
    ) -> Awaitable[DataFrame[TradeSchema]] | list[Awaitable[DataFrame[TradeSchema]]]:
        """Returns a DataFrame[TradeSchema] from ccxt.watch_trades_for_symbols"""
        ...

    def dapiDataGetBasis(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.dapiDataGetBasis"""
        ...

    def dapiDataGetDeliveryPrice(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.dapiDataGetDeliveryPrice"""
        ...

    def dapiDataGetGlobalLongShortAccountRatio(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.dapiDataGetGlobalLongShortAccountRatio"""
        ...

    def dapiDataGetOpenInterestHist(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.dapiDataGetOpenInterestHist"""
        ...

    def dapiDataGetTakerBuySellVol(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.dapiDataGetTakerBuySellVol"""
        ...

    def dapiDataGetTopLongShortAccountRatio(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.dapiDataGetTopLongShortAccountRatio"""
        ...

    def dapiDataGetTopLongShortPositionRatio(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.dapiDataGetTopLongShortPositionRatio"""
        ...

    def dapiPrivateGetAccount(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.dapiPrivateGetAccount"""
        ...

    def dapiPrivateGetAdlQuantile(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.dapiPrivateGetAdlQuantile"""
        ...

    def dapiPrivateGetAllOrders(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.dapiPrivateGetAllOrders"""
        ...

    def dapiPrivateGetBalance(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.dapiPrivateGetBalance"""
        ...

    def dapiPrivateGetCommissionRate(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.dapiPrivateGetCommissionRate"""
        ...

    def dapiPrivateGetForceOrders(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.dapiPrivateGetForceOrders"""
        ...

    def dapiPrivateGetIncome(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.dapiPrivateGetIncome"""
        ...

    def dapiPrivateGetPositionRisk(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.dapiPrivateGetPositionRisk"""
        ...

    def dapiPrivateGetUserTrades(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.dapiPrivateGetUserTrades"""
        ...

    def dapiPublicGetFundingRate(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.dapiPublicGetFundingRate"""
        ...

    def dapiPublicGetOpenInterest(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.dapiPublicGetOpenInterest"""
        ...

    def dapiPublicGetPremiumIndex(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.dapiPublicGetPremiumIndex"""
        ...

    def dapiPublicGetTicker24hr(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.dapiPublicGetTicker24hr"""
        ...

    def dapiPublicGetTickerBookTicker(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.dapiPublicGetTickerBookTicker"""
        ...

    def dapiPublicGetTickerPrice(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.dapiPublicGetTickerPrice"""
        ...

    def fapiDataGetGlobalLongShortAccountRatio(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.fapiDataGetGlobalLongShortAccountRatio"""
        ...

    def fapiDataGetOpenInterestHist(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.fapiDataGetOpenInterestHist"""
        ...

    def fapiDataGetTakerlongshortRatio(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.fapiDataGetTakerlongshortRatio"""
        ...

    def fapiDataGetTopLongShortAccountRatio(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.fapiDataGetTopLongShortAccountRatio"""
        ...

    def fapiDataGetTopLongShortPositionRatio(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.fapiDataGetTopLongShortPositionRatio"""
        ...

    def fapiPrivateDeleteAlgoOpenOrders(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.fapiPrivateDeleteAlgoOpenOrders"""
        ...

    def fapiPrivateDeleteAlgoOrder(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.fapiPrivateDeleteAlgoOrder"""
        ...

    def fapiPrivateGetAccount(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.fapiPrivateGetAccount"""
        ...

    def fapiPrivateGetAdlQuantile(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.fapiPrivateGetAdlQuantile"""
        ...

    def fapiPrivateGetAlgoOrder(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.fapiPrivateGetAlgoOrder"""
        ...

    def fapiPrivateGetAllAlgoOrders(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.fapiPrivateGetAllAlgoOrders"""
        ...

    def fapiPrivateGetAllOrders(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.fapiPrivateGetAllOrders"""
        ...

    def fapiPrivateGetBalance(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.fapiPrivateGetBalance"""
        ...

    def fapiPrivateGetCommissionRate(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.fapiPrivateGetCommissionRate"""
        ...

    def fapiPrivateGetForceOrders(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.fapiPrivateGetForceOrders"""
        ...

    def fapiPrivateGetIncome(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.fapiPrivateGetIncome"""
        ...

    def fapiPrivateGetOpenAlgoOrders(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.fapiPrivateGetOpenAlgoOrders"""
        ...

    def fapiPrivateGetPositionRisk(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.fapiPrivateGetPositionRisk"""
        ...

    def fapiPrivateGetUserTrades(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.fapiPrivateGetUserTrades"""
        ...

    def fapiPrivatePostAlgoOrder(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.fapiPrivatePostAlgoOrder"""
        ...

    def fapiPublicGetFundingRate(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.fapiPublicGetFundingRate"""
        ...

    def fapiPublicGetOpenInterest(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.fapiPublicGetOpenInterest"""
        ...

    def fapiPublicGetPremiumIndex(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.fapiPublicGetPremiumIndex"""
        ...

    def fapiPublicGetTicker24hr(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.fapiPublicGetTicker24hr"""
        ...

    def fapiPublicGetTickerBookTicker(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.fapiPublicGetTickerBookTicker"""
        ...

    def fapiPublicGetTickerPrice(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.fapiPublicGetTickerPrice"""
        ...

    def privateGetAccountBalance(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetAccountBalance"""
        ...

    def privateGetAccountBills(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetAccountBills"""
        ...

    def privateGetAccountBillsArchive(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetAccountBillsArchive"""
        ...

    def privateGetAccountConfig(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetAccountConfig"""
        ...

    def privateGetAccountGreeks(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetAccountGreeks"""
        ...

    def privateGetAccountInterestAccrued(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetAccountInterestAccrued"""
        ...

    def privateGetAccountLeverageInfo(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetAccountLeverageInfo"""
        ...

    def privateGetAccountPositions(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetAccountPositions"""
        ...

    def privateGetAccountPositionsHistory(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetAccountPositionsHistory"""
        ...

    def privateGetFinanceFlexibleLoanBorrowCurrencies(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetFinanceFlexibleLoanBorrowCurrencies"""
        ...

    def privateGetFinanceFlexibleLoanCollateralAssets(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetFinanceFlexibleLoanCollateralAssets"""
        ...

    def privateGetFinanceFlexibleLoanInterestAccrued(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetFinanceFlexibleLoanInterestAccrued"""
        ...

    def privateGetFinanceFlexibleLoanLoanHistory(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetFinanceFlexibleLoanLoanHistory"""
        ...

    def privateGetFinanceFlexibleLoanLoanInfo(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetFinanceFlexibleLoanLoanInfo"""
        ...

    def privateGetFinanceFlexibleLoanMaxCollateralRedeemAmount(
        self, params={}
    ) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetFinanceFlexibleLoanMaxCollateralRedeemAmount"""
        ...

    def privateGetFinanceSavingsBalance(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetFinanceSavingsBalance"""
        ...

    def privateGetFinanceSavingsLendingHistory(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetFinanceSavingsLendingHistory"""
        ...

    def privateGetFinanceStakingDefiEthBalance(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetFinanceStakingDefiEthBalance"""
        ...

    def privateGetFinanceStakingDefiEthProductInfo(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetFinanceStakingDefiEthProductInfo"""
        ...

    def privateGetFinanceStakingDefiEthPurchaseRedeemHistory(
        self, params={}
    ) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetFinanceStakingDefiEthPurchaseRedeemHistory"""
        ...

    def privateGetFinanceStakingDefiOffers(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetFinanceStakingDefiOffers"""
        ...

    def privateGetFinanceStakingDefiOrdersActive(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetFinanceStakingDefiOrdersActive"""
        ...

    def privateGetFinanceStakingDefiOrdersHistory(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetFinanceStakingDefiOrdersHistory"""
        ...

    def privateGetFinanceStakingDefiSolBalance(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetFinanceStakingDefiSolBalance"""
        ...

    def privateGetFinanceStakingDefiSolProductInfo(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetFinanceStakingDefiSolProductInfo"""
        ...

    def privateGetFinanceStakingDefiSolPurchaseRedeemHistory(
        self, params={}
    ) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetFinanceStakingDefiSolPurchaseRedeemHistory"""
        ...

    def privateGetSprdOrder(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetSprdOrder"""
        ...

    def privateGetSprdOrdersHistory(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetSprdOrdersHistory"""
        ...

    def privateGetSprdOrdersHistoryArchive(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetSprdOrdersHistoryArchive"""
        ...

    def privateGetSprdOrdersPending(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetSprdOrdersPending"""
        ...

    def privateGetSprdTrades(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetSprdTrades"""
        ...

    def privateGetTradeFills(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetTradeFills"""
        ...

    def privateGetTradeFillsHistory(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetTradeFillsHistory"""
        ...

    def privateGetTradeOrdersAlgoHistory(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetTradeOrdersAlgoHistory"""
        ...

    def privateGetTradeOrdersAlgoPending(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetTradeOrdersAlgoPending"""
        ...

    def privateGetTradeOrdersHistory(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetTradeOrdersHistory"""
        ...

    def privateGetTradeOrdersHistoryArchive(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetTradeOrdersHistoryArchive"""
        ...

    def privateGetTradeOrdersPending(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetTradeOrdersPending"""
        ...

    def privateGetTradingBotGridOrdersAlgoDetails(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetTradingBotGridOrdersAlgoDetails"""
        ...

    def privateGetTradingBotGridOrdersAlgoHistory(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetTradingBotGridOrdersAlgoHistory"""
        ...

    def privateGetTradingBotGridOrdersAlgoPending(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetTradingBotGridOrdersAlgoPending"""
        ...

    def privateGetTradingBotGridPositions(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetTradingBotGridPositions"""
        ...

    def privateGetTradingBotGridSubOrders(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetTradingBotGridSubOrders"""
        ...

    def privateGetTradingBotRecurringOrdersAlgoDetails(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetTradingBotRecurringOrdersAlgoDetails"""
        ...

    def privateGetTradingBotRecurringOrdersAlgoHistory(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetTradingBotRecurringOrdersAlgoHistory"""
        ...

    def privateGetTradingBotRecurringOrdersAlgoPending(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetTradingBotRecurringOrdersAlgoPending"""
        ...

    def privateGetTradingBotRecurringSubOrders(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetTradingBotRecurringSubOrders"""
        ...

    def privateGetTradingBotSignalOrdersAlgoDetails(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetTradingBotSignalOrdersAlgoDetails"""
        ...

    def privateGetTradingBotSignalOrdersAlgoHistory(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetTradingBotSignalOrdersAlgoHistory"""
        ...

    def privateGetTradingBotSignalOrdersAlgoPending(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetTradingBotSignalOrdersAlgoPending"""
        ...

    def privateGetTradingBotSignalPositions(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetTradingBotSignalPositions"""
        ...

    def privateGetTradingBotSignalPositionsHistory(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetTradingBotSignalPositionsHistory"""
        ...

    def privateGetTradingBotSignalSubOrders(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privateGetTradingBotSignalSubOrders"""
        ...

    def privatePostFinanceFlexibleLoanAdjustCollateral(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privatePostFinanceFlexibleLoanAdjustCollateral"""
        ...

    def privatePostFinanceFlexibleLoanMaxLoan(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privatePostFinanceFlexibleLoanMaxLoan"""
        ...

    def privatePostFinanceSavingsPurchaseRedempt(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privatePostFinanceSavingsPurchaseRedempt"""
        ...

    def privatePostFinanceSavingsSetLendingRate(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privatePostFinanceSavingsSetLendingRate"""
        ...

    def privatePostFinanceStakingDefiEthCancelRedeem(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privatePostFinanceStakingDefiEthCancelRedeem"""
        ...

    def privatePostFinanceStakingDefiEthPurchase(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privatePostFinanceStakingDefiEthPurchase"""
        ...

    def privatePostFinanceStakingDefiEthRedeem(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privatePostFinanceStakingDefiEthRedeem"""
        ...

    def privatePostFinanceStakingDefiSolCancelRedeem(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privatePostFinanceStakingDefiSolCancelRedeem"""
        ...

    def privatePostFinanceStakingDefiSolPurchase(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privatePostFinanceStakingDefiSolPurchase"""
        ...

    def privatePostFinanceStakingDefiSolRedeem(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privatePostFinanceStakingDefiSolRedeem"""
        ...

    def privatePostSprdAmendOrder(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privatePostSprdAmendOrder"""
        ...

    def privatePostSprdCancelAllAfter(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privatePostSprdCancelAllAfter"""
        ...

    def privatePostSprdCancelOrder(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privatePostSprdCancelOrder"""
        ...

    def privatePostSprdMassCancel(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privatePostSprdMassCancel"""
        ...

    def privatePostSprdOrder(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.privatePostSprdOrder"""
        ...

    def publicGetFinanceSavingsLendingRateHistory(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetFinanceSavingsLendingRateHistory"""
        ...

    def publicGetFinanceSavingsLendingRateSummary(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetFinanceSavingsLendingRateSummary"""
        ...

    def publicGetFinanceStakingDefiEthApyHistory(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetFinanceStakingDefiEthApyHistory"""
        ...

    def publicGetFinanceStakingDefiSolApyHistory(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetFinanceStakingDefiSolApyHistory"""
        ...

    def publicGetMarketBlockTicker(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetMarketBlockTicker"""
        ...

    def publicGetMarketBlockTickers(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetMarketBlockTickers"""
        ...

    def publicGetMarketCandles(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetMarketCandles"""
        ...

    def publicGetMarketExchangeRate(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetMarketExchangeRate"""
        ...

    def publicGetMarketHistoryCandles(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetMarketHistoryCandles"""
        ...

    def publicGetMarketHistoryIndexCandles(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetMarketHistoryIndexCandles"""
        ...

    def publicGetMarketHistoryMarkPriceCandles(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetMarketHistoryMarkPriceCandles"""
        ...

    def publicGetMarketHistoryTrades(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetMarketHistoryTrades"""
        ...

    def publicGetMarketIndexCandles(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetMarketIndexCandles"""
        ...

    def publicGetMarketIndexTickers(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetMarketIndexTickers"""
        ...

    def publicGetMarketMarkPriceCandles(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetMarketMarkPriceCandles"""
        ...

    def publicGetMarketPlatform24Volume(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetMarketPlatform24Volume"""
        ...

    def publicGetMarketSprdCandles(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetMarketSprdCandles"""
        ...

    def publicGetMarketSprdHistoryCandles(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetMarketSprdHistoryCandles"""
        ...

    def publicGetMarketTicker(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetMarketTicker"""
        ...

    def publicGetMarketTickers(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetMarketTickers"""
        ...

    def publicGetMarketTrades(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetMarketTrades"""
        ...

    def publicGetPublicDeliveryExerciseHistory(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetPublicDeliveryExerciseHistory"""
        ...

    def publicGetPublicEstimatedPrice(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetPublicEstimatedPrice"""
        ...

    def publicGetPublicFundingRate(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetPublicFundingRate"""
        ...

    def publicGetPublicFundingRateHistory(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetPublicFundingRateHistory"""
        ...

    def publicGetPublicInstruments(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetPublicInstruments"""
        ...

    def publicGetPublicInsuranceFund(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetPublicInsuranceFund"""
        ...

    def publicGetPublicMarkPrice(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetPublicMarkPrice"""
        ...

    def publicGetPublicOpenInterest(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetPublicOpenInterest"""
        ...

    def publicGetPublicOptSummary(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetPublicOptSummary"""
        ...

    def publicGetPublicPositionTiers(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetPublicPositionTiers"""
        ...

    def publicGetPublicPremiumHistory(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetPublicPremiumHistory"""
        ...

    def publicGetPublicPriceLimit(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetPublicPriceLimit"""
        ...

    def publicGetPublicSettlementHistory(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetPublicSettlementHistory"""
        ...

    def publicGetRubikStatContractsLongShortAccountRatio(
        self, params={}
    ) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetRubikStatContractsLongShortAccountRatio"""
        ...

    def publicGetRubikStatContractsLongShortAccountRatioContract(
        self, params={}
    ) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetRubikStatContractsLongShortAccountRatioContract"""
        ...

    def publicGetRubikStatContractsLongShortAccountRatioContractTopTrader(
        self, params={}
    ) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetRubikStatContractsLongShortAccountRatioContractTopTrader"""
        ...

    def publicGetRubikStatContractsOpenInterestHistory(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetRubikStatContractsOpenInterestHistory"""
        ...

    def publicGetRubikStatContractsOpenInterestVolume(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetRubikStatContractsOpenInterestVolume"""
        ...

    def publicGetRubikStatMarginLoanRatio(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetRubikStatMarginLoanRatio"""
        ...

    def publicGetRubikStatOptionOpenInterestVolume(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetRubikStatOptionOpenInterestVolume"""
        ...

    def publicGetRubikStatOptionOpenInterestVolumeExpiry(
        self, params={}
    ) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetRubikStatOptionOpenInterestVolumeExpiry"""
        ...

    def publicGetRubikStatOptionOpenInterestVolumeRatio(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetRubikStatOptionOpenInterestVolumeRatio"""
        ...

    def publicGetRubikStatOptionOpenInterestVolumeStrike(
        self, params={}
    ) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetRubikStatOptionOpenInterestVolumeStrike"""
        ...

    def publicGetRubikStatOptionTakerBlockVolume(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetRubikStatOptionTakerBlockVolume"""
        ...

    def publicGetRubikStatTakerVolume(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetRubikStatTakerVolume"""
        ...

    def publicGetRubikStatTakerVolumeContract(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetRubikStatTakerVolumeContract"""
        ...

    def publicGetSprdPublicTrades(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetSprdPublicTrades"""
        ...

    def publicGetSprdSpreads(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetSprdSpreads"""
        ...

    def publicGetSprdTicker(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.publicGetSprdTicker"""
        ...

    def sapiDeleteAlgoFuturesOrder(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiDeleteAlgoFuturesOrder"""
        ...

    def sapiDeleteAlgoSpotOrder(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiDeleteAlgoSpotOrder"""
        ...

    def sapiGetAccumulatorProductList(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiGetAccumulatorProductList"""
        ...

    def sapiGetAccumulatorProductPositionList(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiGetAccumulatorProductPositionList"""
        ...

    def sapiGetAccumulatorProductSumHolding(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiGetAccumulatorProductSumHolding"""
        ...

    def sapiGetAlgoFuturesHistoricalOrders(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiGetAlgoFuturesHistoricalOrders"""
        ...

    def sapiGetAlgoFuturesOpenOrders(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiGetAlgoFuturesOpenOrders"""
        ...

    def sapiGetAlgoFuturesSubOrders(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiGetAlgoFuturesSubOrders"""
        ...

    def sapiGetAlgoSpotHistoricalOrders(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiGetAlgoSpotHistoricalOrders"""
        ...

    def sapiGetAlgoSpotOpenOrders(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiGetAlgoSpotOpenOrders"""
        ...

    def sapiGetAlgoSpotSubOrders(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiGetAlgoSpotSubOrders"""
        ...

    def sapiGetDciProductAccounts(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiGetDciProductAccounts"""
        ...

    def sapiGetDciProductList(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiGetDciProductList"""
        ...

    def sapiGetDciProductPositions(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiGetDciProductPositions"""
        ...

    def sapiGetSimpleEarnAccount(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiGetSimpleEarnAccount"""
        ...

    def sapiGetSimpleEarnFlexibleHistoryRedemptionRecord(
        self, params={}
    ) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiGetSimpleEarnFlexibleHistoryRedemptionRecord"""
        ...

    def sapiGetSimpleEarnFlexibleHistoryRewardsRecord(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiGetSimpleEarnFlexibleHistoryRewardsRecord"""
        ...

    def sapiGetSimpleEarnFlexibleHistorySubscriptionRecord(
        self, params={}
    ) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiGetSimpleEarnFlexibleHistorySubscriptionRecord"""
        ...

    def sapiGetSimpleEarnFlexibleList(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiGetSimpleEarnFlexibleList"""
        ...

    def sapiGetSimpleEarnFlexiblePosition(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiGetSimpleEarnFlexiblePosition"""
        ...

    def sapiGetSimpleEarnLockedHistoryRedemptionRecord(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiGetSimpleEarnLockedHistoryRedemptionRecord"""
        ...

    def sapiGetSimpleEarnLockedHistoryRewardsRecord(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiGetSimpleEarnLockedHistoryRewardsRecord"""
        ...

    def sapiGetSimpleEarnLockedHistorySubscriptionRecord(
        self, params={}
    ) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiGetSimpleEarnLockedHistorySubscriptionRecord"""
        ...

    def sapiGetSimpleEarnLockedList(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiGetSimpleEarnLockedList"""
        ...

    def sapiGetSimpleEarnLockedPosition(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiGetSimpleEarnLockedPosition"""
        ...

    def sapiPostAccumulatorProductSubscribe(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiPostAccumulatorProductSubscribe"""
        ...

    def sapiPostAlgoFuturesNewOrderTwap(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiPostAlgoFuturesNewOrderTwap"""
        ...

    def sapiPostAlgoFuturesNewOrderVp(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiPostAlgoFuturesNewOrderVp"""
        ...

    def sapiPostAlgoSpotNewOrderTwap(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiPostAlgoSpotNewOrderTwap"""
        ...

    def sapiPostDciProductAutoCompoundEdit(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiPostDciProductAutoCompoundEdit"""
        ...

    def sapiPostDciProductSubscribe(self, params={}) -> Awaitable[pd.DataFrame]:
        """Returns a pd.DataFrame from ccxt.sapiPostDciProductSubscribe"""
        ...
