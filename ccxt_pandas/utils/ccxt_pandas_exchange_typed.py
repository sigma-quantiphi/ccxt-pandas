from typing import Literal, Protocol
from decimal import Decimal
import pandas as pd


class CCXTPandasExchangeTyped(Protocol):
    """A Class to add type hinting to CCXTPandasExchangeTyped"""

    def cancel_all_orders(
        self, symbol: str | list[str] = None, params={}
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.cancel_all_orders"""
        ...

    def cancel_all_orders_ws(
        self, symbol: str | list[str] = None, params={}
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.cancel_all_orders_ws"""
        ...

    def cancel_order(self, id: str, symbol: str | list[str] = None, params={}) -> dict:
        """Returns a dict from ccxt.cancel_order"""
        ...

    def cancel_order_ws(
        self, id: str, symbol: str | list[str] = None, params={}
    ) -> dict:
        """Returns a dict from ccxt.cancel_order_ws"""
        ...

    def cancel_orders(
        self, ids: list[str], symbol: str | list[str] = None, params={}
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.cancel_orders"""
        ...

    def cancel_orders_for_symbols(
        self, orders: pd.DataFrame, params={}
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.cancel_orders_for_symbols"""
        ...

    def cancel_orders_ws(
        self, ids: list[str], symbol: str | list[str] = None, params={}
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.cancel_orders_ws"""
        ...

    def create_order(
        self,
        symbol: str | list[str],
        type: Literal["limit", "market"],
        side: Literal["buy", "sell"],
        amount: float,
        price: None | str | float | int | Decimal = None,
        params={},
    ) -> dict:
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
    ) -> dict:
        """Returns a dict from ccxt.create_order_ws"""
        ...

    def create_orders(self, orders: pd.DataFrame, params={}) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.create_orders"""
        ...

    def create_orders_ws(self, orders: pd.DataFrame, params={}) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.create_orders_ws"""
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
    ) -> dict:
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
    ) -> dict:
        """Returns a dict from ccxt.edit_order_ws"""
        ...

    def edit_orders(self, orders: pd.DataFrame, params={}) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.edit_orders"""
        ...

    def fetch_accounts(self, params={}) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_accounts"""
        ...

    def fetch_all_greeks(
        self, symbols: list[str] | None = None, params={}
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_all_greeks"""
        ...

    def fetch_balance(self, params={}) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_balance"""
        ...

    def fetch_bids_asks(
        self, symbols: list[str] | None = None, params={}
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_bids_asks"""
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
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_borrow_interest"""
        ...

    def fetch_canceled_and_closed_orders(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_canceled_and_closed_orders"""
        ...

    def fetch_canceled_orders(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_canceled_orders"""
        ...

    def fetch_closed_orders(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_closed_orders"""
        ...

    def fetch_convert_currencies(self, params={}) -> pd.DataFrame:
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
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_convert_trade_history"""
        ...

    def fetch_cross_borrow_rate(self, code: str | list[str], params={}) -> dict:
        """Returns a dict from ccxt.fetch_cross_borrow_rate"""
        ...

    def fetch_cross_borrow_rates(self, params={}) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_cross_borrow_rates"""
        ...

    def fetch_currencies(self, params={}) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_currencies"""
        ...

    def fetch_deposit_addresses(
        self, codes: list[str] | None = None, params={}
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_deposit_addresses"""
        ...

    def fetch_deposit_withdraw_fee(self, code: str | list[str], params={}) -> dict:
        """Returns a dict from ccxt.fetch_deposit_withdraw_fee"""
        ...

    def fetch_deposit_withdraw_fees(
        self, codes: list[str] | None = None, params={}
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_deposit_withdraw_fees"""
        ...

    def fetch_deposits(
        self,
        code: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_deposits"""
        ...

    def fetch_deposits_withdrawals(
        self,
        code: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_deposits_withdrawals"""
        ...

    def fetch_funding_history(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_funding_history"""
        ...

    def fetch_funding_interval(self, symbol: str | list[str], params={}) -> dict:
        """Returns a dict from ccxt.fetch_funding_interval"""
        ...

    def fetch_funding_intervals(
        self, symbols: list[str] | None = None, params={}
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_funding_intervals"""
        ...

    def fetch_funding_rate(self, symbol: str | list[str], params={}) -> dict:
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
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_funding_rate_history"""
        ...

    def fetch_funding_rates(
        self, symbols: list[str] | None = None, params={}
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_funding_rates"""
        ...

    def fetch_greeks(self, symbol: str | list[str], params={}) -> dict:
        """Returns a dict from ccxt.fetch_greeks"""
        ...

    def fetch_isolated_borrow_rate(self, symbol: str | list[str], params={}) -> dict:
        """Returns a dict from ccxt.fetch_isolated_borrow_rate"""
        ...

    def fetch_isolated_borrow_rates(self, params={}) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_isolated_borrow_rates"""
        ...

    def fetch_last_prices(
        self, symbols: list[str] | None = None, params={}
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_last_prices"""
        ...

    def fetch_ledger(
        self,
        code: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_ledger"""
        ...

    def fetch_leverage_tiers(
        self, symbols: list[str] | None = None, params={}
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_leverage_tiers"""
        ...

    def fetch_leverages(
        self, symbols: list[str] | None = None, params={}
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_leverages"""
        ...

    def fetch_liquidations(
        self,
        symbol: str | list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_liquidations"""
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
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_long_short_ratio_history"""
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
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_margin_adjustment_history"""
        ...

    def fetch_margin_modes(
        self, symbols: list[str] | None = None, params={}
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_margin_modes"""
        ...

    def fetch_mark_price(self, symbol: str | list[str], params={}) -> dict:
        """Returns a dict from ccxt.fetch_mark_price"""
        ...

    def fetch_mark_prices(
        self, symbols: list[str] | None = None, params={}
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_mark_prices"""
        ...

    def fetch_markets(self, params={}) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_markets"""
        ...

    def fetch_my_liquidations(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_my_liquidations"""
        ...

    def fetch_my_trades(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_my_trades"""
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
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_ohlcv"""
        ...

    def fetch_open_interest(self, symbol: str | list[str], params={}) -> dict:
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
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_open_interest_history"""
        ...

    def fetch_open_interests(
        self, symbols: list[str] | None = None, params={}
    ) -> pd.DataFrame:
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
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_open_orders"""
        ...

    def fetch_option(self, symbol: str | list[str], params={}) -> dict:
        """Returns a dict from ccxt.fetch_option"""
        ...

    def fetch_option_chain(self, code: str | list[str], params={}) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_option_chain"""
        ...

    def fetch_order(self, id: str, symbol: str | list[str] = None, params={}) -> dict:
        """Returns a dict from ccxt.fetch_order"""
        ...

    def fetch_order_book(
        self, symbol: str | list[str], limit: int | None = None, params={}
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_order_book"""
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
    ) -> pd.DataFrame:
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
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_orders"""
        ...

    def fetch_orders_ws(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_orders_ws"""
        ...

    def fetch_position(self, symbol: str | list[str], params={}) -> dict:
        """Returns a dict from ccxt.fetch_position"""
        ...

    def fetch_position_history(
        self,
        symbol: str | list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_position_history"""
        ...

    def fetch_positions(
        self, symbols: list[str] | None = None, params={}
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_positions"""
        ...

    def fetch_positions_history(
        self,
        symbols: list[str] | None = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        limit: int | None = None,
        params={},
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_positions_history"""
        ...

    def fetch_positions_risk(
        self, symbols: list[str] | None = None, params={}
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_positions_risk"""
        ...

    def fetch_status(self, params={}) -> dict:
        """Returns a dict from ccxt.fetch_status"""
        ...

    def fetch_ticker(self, symbol: str | list[str], params={}) -> dict:
        """Returns a dict from ccxt.fetch_ticker"""
        ...

    def fetch_tickers(
        self, symbols: list[str] | None = None, params={}
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_tickers"""
        ...

    def fetch_trades(
        self,
        symbol: str | list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_trades"""
        ...

    def fetch_trading_fee(self, symbol: str | list[str], params={}) -> dict:
        """Returns a dict from ccxt.fetch_trading_fee"""
        ...

    def fetch_trading_fees(self, params={}) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_trading_fees"""
        ...

    def fetch_transaction_fees(
        self, codes: list[str] | None = None, params={}
    ) -> pd.DataFrame:
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
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_transfers"""
        ...

    def fetch_withdrawals(
        self,
        code: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.fetch_withdrawals"""
        ...

    def load_markets(self, reload=False, params={}) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.load_markets"""
        ...

    def watch_balance(self, params={}) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.watch_balance"""
        ...

    def watch_bids_asks(
        self, symbols: list[str] | None = None, params={}
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.watch_bids_asks"""
        ...

    def watch_funding_rate(self, symbol: str | list[str], params={}) -> dict:
        """Returns a dict from ccxt.watch_funding_rate"""
        ...

    def watch_funding_rates(self, symbols: list[str], params={}) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.watch_funding_rates"""
        ...

    def watch_liquidations(
        self,
        symbol: str | list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.watch_liquidations"""
        ...

    def watch_liquidations_for_symbols(
        self,
        symbols: list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        limit: int | None = None,
        params={},
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.watch_liquidations_for_symbols"""
        ...

    def watch_mark_price(self, symbol: str | list[str], params={}) -> dict:
        """Returns a dict from ccxt.watch_mark_price"""
        ...

    def watch_mark_prices(
        self, symbols: list[str] | None = None, params={}
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.watch_mark_prices"""
        ...

    def watch_my_liquidations(
        self,
        symbol: str | list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.watch_my_liquidations"""
        ...

    def watch_my_liquidations_for_symbols(
        self,
        symbols: list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        limit: int | None = None,
        params={},
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.watch_my_liquidations_for_symbols"""
        ...

    def watch_my_trades(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.watch_my_trades"""
        ...

    def watch_my_trades_for_symbols(
        self,
        symbols: list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        limit: int | None = None,
        params={},
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.watch_my_trades_for_symbols"""
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
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.watch_ohlcv"""
        ...

    def watch_ohlcv_for_symbols(
        self,
        symbolsAndTimeframes: list[list[str]],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        limit: int | None = None,
        params={},
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.watch_ohlcv_for_symbols"""
        ...

    def watch_order_book(
        self, symbol: str | list[str], limit: int | None = None, params={}
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.watch_order_book"""
        ...

    def watch_order_book_for_symbols(
        self, symbols: list[str], limit: int | None = None, params={}
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.watch_order_book_for_symbols"""
        ...

    def watch_orders(
        self,
        symbol: str | list[str] = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.watch_orders"""
        ...

    def watch_orders_for_symbols(
        self,
        symbols: list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        limit: int | None = None,
        params={},
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.watch_orders_for_symbols"""
        ...

    def watch_position(self, symbol: str | list[str] = None, params={}) -> dict:
        """Returns a dict from ccxt.watch_position"""
        ...

    def watch_positions(
        self,
        symbols: list[str] | None = None,
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        limit: int | None = None,
        params={},
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.watch_positions"""
        ...

    def watch_ticker(self, symbol: str | list[str], params={}) -> dict:
        """Returns a dict from ccxt.watch_ticker"""
        ...

    def watch_tickers(
        self, symbols: list[str] | None = None, params={}
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.watch_tickers"""
        ...

    def watch_trades(
        self,
        symbol: str | list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        cache: bool = False,
        limit: int | None = None,
        params={},
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.watch_trades"""
        ...

    def watch_trades_for_symbols(
        self,
        symbols: list[str],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        limit: int | None = None,
        params={},
    ) -> pd.DataFrame:
        """Returns a pd.DataFrame from ccxt.watch_trades_for_symbols"""
        ...
