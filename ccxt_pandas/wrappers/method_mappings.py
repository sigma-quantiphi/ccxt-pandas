from typing import Dict, Optional, Type, Any

import pandera as pa

from ccxt_pandas.utils.utils import add_camel_case_methods
from ccxt_pandas.wrappers.schemas import AccountsSchema, AddressesSchema, BalanceSchema, BidsAsksSchema, \
    BorrowInterestSchema, CrossBorrowRatesSchema, CurrencySchema, IsolatedBorrowRatesSchema

standard_dataframe_methods = {
    "fetch_accounts",
    "fetch_account_positions",
    "fetch_portfolio_details",
    "fetch_portfolios",
    "cancel_all_orders",
    "cancel_all_orders_ws",
    "cancel_orders",
    "cancel_orders_ws",
    "cancel_orders_for_symbols",
    "create_orders",
    "create_orders_ws",
    "edit_orders",
    "edit_orders_ws",
    "fetch_borrow_interest",
    "fetch_borrow_rate_histories",
    "fetch_borrow_rate_history",
    "fetch_convert_trade_history",
    "fetch_cross_borrow_rates",
    "fetch_deposit_addresses",
    "fetch_deposits",
    "fetch_deposits_withdrawals",
    "fetch_funding_history",
    "fetch_funding_rate_history",
    "fetch_ledger",
    "fetch_leverage_tiers",
    "fetch_liquidations",
    "fetch_long_short_ratio_history",
    "fetch_margin_adjustment_history",
    "fetch_margin_modes",
    "fetch_markets",
    "fetch_my_dust_trades",
    "fetch_my_liquidations",
    "fetch_my_trades",
    "fetch_open_interest_history",
    "fetch_option_positions",
    "fetch_order_trades",
    "fetch_position_history",
    "fetch_positions",
    "fetch_positions_history",
    "fetch_positions_risk",
    "fetch_settlement_history",
    "fetch_trades",
    "fetch_transfers",
    "fetch_volatility_history",
    "fetch_withdrawals",
    "watch_liquidations",
    "watch_liquidations_for_symbols",
    "watch_my_liquidations",
    "watch_my_liquidations_for_symbols",
    "watch_my_trades",
    "watch_my_trades_for_symbols",
    "watch_positions",
    "watch_trades",
    "watch_trades_for_symbols",
}
markets_dataframe_methods = {
    "fetch_all_greeks",
    "fetch_bids_asks",
    "fetch_convert_currencies",
    "fetch_funding_intervals",
    "fetch_funding_rates",
    "fetch_isolated_borrow_rates",
    "fetch_last_prices",
    "fetch_leverages",
    "fetch_mark_prices",
    "fetch_open_interests",
    "fetch_option_chain",
    "fetch_tickers",
    "fetch_trading_fees",
    "fetch_transaction_fees",
    "load_markets",
    "watch_bids_asks",
    "watch_funding_rates",
    "watch_mark_prices",
    "watch_tickers",
}
currencies_dataframe_methods = {"fetch_currencies", "fetch_deposit_withdraw_fees"}
balance_dataframe_methods = {"fetch_balance", "watch_balance"}
ohlcv_dataframe_methods = {"fetch_ohlcv", "fetchOHLCV", "watch_ohlcv", "watchOHLCV"}
ohlcv_symbols_dataframe_methods = {"watch_ohlcv_for_symbols", "watchOHLCVForSymbols"}
orderbook_dataframe_methods = {
    "fetch_order_book",
    "fetch_l3_order_book",
    "watch_order_book",
    "watch_order_book_for_symbols",
}
orderbooks_dataframe_methods = {"fetch_order_books"}
orders_dataframe_methods = {
    "fetch_canceled_and_closed_orders",
    "fetch_canceled_orders",
    "fetch_closed_orders",
    "fetch_open_orders",
    "fetch_orders",
    "fetch_orders_by_ids",
    "fetch_orders_by_status",
    "fetch_orders_classic",
    "fetch_orders_ws",
    "watch_orders",
    "watch_orders_for_symbols",
}
dict_methods = {
    "cancel_order",
    "cancel_order_ws",
    "create_order",
    "create_order_ws",
    "edit_order",
    "edit_order_ws",
    "fetch_cross_borrow_rate",
    "fetch_deposit",
    "fetch_funding_interval",
    "fetch_funding_rate",
    "fetch_greeks",
    "fetch_isolated_borrow_rate",
    "fetch_mark_price",
    "fetch_open_interest",
    "fetch_option",
    "fetch_order",
    "fetch_position",
    "fetch_status",
    "fetch_ticker",
    "fetch_trade",
    "fetch_trading_fee",
    "fetch_deposit_withdraw_fee",
    "watch_funding_rate",
    "watch_mark_price",
    "watch_position",
    "watch_ticker",
}
single_order_methods = {
    "create_order",
    "edit_order",
    "create_order_ws",
    "edit_order_ws",
}
bulk_order_methods = {
    "create_orders",
    "edit_orders",
    "create_orders_ws",
    "edit_orders_ws",
}
symbol_order_methods = {"cancel_orders_for_symbols"}
orders_methods = {
    "create_order",
    "edit_order",
    "cancel_order",
    "create_orders",
    "edit_orders",
    "cancel_orders",
    "cancel_orders_for_symbols",
}
standard_dataframe_methods = add_camel_case_methods(standard_dataframe_methods)
standard_dataframe_methods.update({"fetch_positions_adl_rank", "fetchPositionsADLRank"})
markets_dataframe_methods = add_camel_case_methods(markets_dataframe_methods)
currencies_dataframe_methods = add_camel_case_methods(currencies_dataframe_methods)
balance_dataframe_methods = add_camel_case_methods(balance_dataframe_methods)
orderbook_dataframe_methods = add_camel_case_methods(orderbook_dataframe_methods)
orderbooks_dataframe_methods = add_camel_case_methods(orderbooks_dataframe_methods)
orders_dataframe_methods = add_camel_case_methods(orders_dataframe_methods)
dict_methods = add_camel_case_methods(dict_methods)
dict_methods.update({"fetch_adl_rank", "fetch_position_adl_rank", "fetchADLRank", "fetchPositionADLRank"})
single_order_methods = add_camel_case_methods(single_order_methods)
bulk_order_methods = add_camel_case_methods(bulk_order_methods)
symbol_order_methods = add_camel_case_methods(symbol_order_methods)
orders_methods = add_camel_case_methods(orders_methods)
dataframe_methods = (
    standard_dataframe_methods
    | markets_dataframe_methods
    | currencies_dataframe_methods
    | balance_dataframe_methods
    | ohlcv_dataframe_methods
    | ohlcv_symbols_dataframe_methods
    | orderbook_dataframe_methods
    | orderbooks_dataframe_methods
    | orders_dataframe_methods
)
modified_methods = dataframe_methods | dict_methods


# Schema mapping for validation
# Import schemas (lazy import to avoid circular dependencies)
def _get_schemas() -> dict[str | Any, type[
    AccountsSchema | AddressesSchema | BalanceSchema | BidsAsksSchema | BorrowInterestSchema | CrossBorrowRatesSchema | IsolatedBorrowRatesSchema | CurrencySchema] | Any]:
    """Get schema mapping. Lazy import to avoid circular dependencies."""
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
        MarkPricesSchema,
        MarketSchema,
        MyTradesSchema,
        OHLCVSchema,
        OpenInterestHistorySchema,
        OrderBookSchema,
        OrdersSchema,
        OrderSchema,
        PortfolioDetailsSchema,
        PortfoliosSchema,
        PositionsADLRankSchema,
        PositionsHistorySchema,
        PositionsSchema,
        TickersSchema,
        TradeSchema,
        TradingFeesSchema,
        TransactionsSchema,
        TransfersSchema,
        VolatilityHistorySchema,
    )

    return {
        # Accounts
        "fetch_accounts": AccountsSchema,
        # Addresses
        "fetch_deposit_addresses": AddressesSchema,
        # Balance
        "fetch_balance": BalanceSchema,
        "watch_balance": BalanceSchema,
        # Bids/Asks
        "fetch_bids_asks": BidsAsksSchema,
        "watch_bids_asks": BidsAsksSchema,
        # Borrow interest
        "fetch_borrow_interest": BorrowInterestSchema,
        # Borrow rates
        "fetch_cross_borrow_rates": CrossBorrowRatesSchema,
        "fetch_isolated_borrow_rates": IsolatedBorrowRatesSchema,
        # Currencies
        "fetch_currencies": CurrencySchema,
        "fetch_deposit_withdraw_fees": DepositWithdrawFeesSchema,
        # Funding
        "fetch_funding_history": FundingHistorySchema,
        "fetch_funding_intervals": FundingIntervalsSchema,
        "fetch_funding_rate_history": FundingRateHistorySchema,
        "fetch_funding_rates": FundingRateSchema,
        "watch_funding_rates": FundingRateSchema,
        # Greeks
        "fetch_all_greeks": GreeksSchema,
        # Last prices
        "fetch_last_prices": LastPricesSchema,
        # Ledger
        "fetch_ledger": LedgerSchema,
        # Leverages
        "fetch_leverages": LeveragesSchema,
        # Liquidations
        "fetch_liquidations": LiquidationsSchema,
        "fetch_my_liquidations": LiquidationsSchema,
        "watch_liquidations": LiquidationsSchema,
        "watch_liquidations_for_symbols": LiquidationsSchema,
        "watch_my_liquidations": LiquidationsSchema,
        "watch_my_liquidations_for_symbols": LiquidationsSchema,
        # Long/short ratio
        "fetch_long_short_ratio_history": LongShortRatioSchema,
        # Mark prices
        "fetch_mark_prices": MarkPricesSchema,
        "watch_mark_prices": MarkPricesSchema,
        # Markets
        "load_markets": MarketSchema,
        "fetch_markets": MarketSchema,
        # OHLCV
        "fetch_ohlcv": OHLCVSchema,
        "watch_ohlcv": OHLCVSchema,
        "watch_ohlcv_for_symbols": OHLCVSchema,
        # Open interest
        "fetch_open_interest_history": OpenInterestHistorySchema,
        # Order book
        "fetch_order_book": OrderBookSchema,
        "fetch_l3_order_book": OrderBookSchema,
        "watch_order_book": OrderBookSchema,
        "watch_order_book_for_symbols": OrderBookSchema,
        # Orders
        "fetch_canceled_and_closed_orders": OrdersSchema,
        "fetch_canceled_orders": OrdersSchema,
        "fetch_closed_orders": OrdersSchema,
        "fetch_open_orders": OrdersSchema,
        "fetch_orders": OrdersSchema,
        "fetch_orders_by_ids": OrdersSchema,
        "fetch_orders_by_status": OrdersSchema,
        "fetch_orders_classic": OrdersSchema,
        "fetch_orders_ws": OrdersSchema,
        "watch_orders": OrdersSchema,
        "watch_orders_for_symbols": OrdersSchema,
        # Single order (dict methods)
        "fetch_order": OrderSchema,
        "create_order": OrderSchema,
        "edit_order": OrderSchema,
        "cancel_order": OrderSchema,
        "create_order_ws": OrderSchema,
        "edit_order_ws": OrderSchema,
        "cancel_order_ws": OrderSchema,
        # Portfolio
        "fetch_portfolio_details": PortfolioDetailsSchema,
        "fetch_portfolios": PortfoliosSchema,
        # Positions
        "fetch_positions": PositionsSchema,
        "fetch_positions_adl_rank": PositionsADLRankSchema,
        "fetch_position_history": PositionsHistorySchema,
        "fetch_positions_history": PositionsHistorySchema,
        "watch_positions": PositionsSchema,
        # Tickers
        "fetch_tickers": TickersSchema,
        "watch_tickers": TickersSchema,
        # Trades
        "fetch_trades": TradeSchema,
        "watch_trades": TradeSchema,
        "watch_trades_for_symbols": TradeSchema,
        # My trades
        "fetch_my_trades": MyTradesSchema,
        "watch_my_trades": MyTradesSchema,
        "watch_my_trades_for_symbols": MyTradesSchema,
        # Trading fees
        "fetch_trading_fees": TradingFeesSchema,
        # Transactions
        "fetch_deposits": TransactionsSchema,
        "fetch_withdrawals": TransactionsSchema,
        "fetch_deposits_withdrawals": TransactionsSchema,
        # Transfers
        "fetch_transfers": TransfersSchema,
        # Volatility
        "fetch_volatility_history": VolatilityHistorySchema,
    }


# Cached schema mapping
_method_schemas_cache: Optional[Dict[str, Type[pa.DataFrameModel]]] = None


def get_method_schema(method_name: str) -> Optional[Type[pa.DataFrameModel]]:
    """Get schema for a method name.

    Args:
        method_name: Method name (e.g., 'fetch_balance', 'fetchBalance')

    Returns:
        Schema class if found, None otherwise
    """
    global _method_schemas_cache

    if _method_schemas_cache is None:
        _method_schemas_cache = _get_schemas()
        # Add camelCase variants
        camel_schemas = {}
        for snake_name, schema in _method_schemas_cache.items():
            # Convert to camelCase
            parts = snake_name.split("_")
            camel_name = parts[0] + "".join(p.capitalize() for p in parts[1:])
            camel_schemas[camel_name] = schema
        _method_schemas_cache.update(camel_schemas)

    return _method_schemas_cache.get(method_name)
