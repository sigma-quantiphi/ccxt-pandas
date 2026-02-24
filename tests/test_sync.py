import os

import ccxt
import pytest
import pandas as pd
from dotenv import load_dotenv

from ccxt_pandas.wrappers.ccxt_pandas_exchange import CCXTPandasExchange

load_dotenv()
spot_symbol = "BNB/USDT"
spot_symbol_list = ["BTC/USDT", "ETH/USDT"]
swap_symbol = "BTC/USDT:USDT"
swap_symbol_list = ["BTC/USDT:USDT", "ETH/USDT:USDT"]
sandbox_settings = {
    "apiKey": os.getenv("SANDBOX_API_KEY"),
    "secret": os.getenv("SANDBOX_API_SECRET"),
    "options": {
        "defaultType": "spot",
        "loadAllOptions": True,
    },
}
settings = {
    "apiKey": os.getenv("API_KEY"),
    "secret": os.getenv("API_SECRET"),
    "options": {
        "defaultType": "future",
        "loadAllOptions": True,
    },
}
okx_settings = {
    "apiKey": os.getenv("OKX_API_KEY"),
    "secret": os.getenv("OKX_API_SECRET"),
    "password": os.getenv("OKX_API_PASSWORD"),
}
coinbase_settings = {
    "apiKey": os.getenv("COINBASE_API_KEY"),
    "secret": (os.getenv("COINBASE_API_SECRET") or "").replace("\\n", "\n"),
}


@pytest.fixture(scope="module")
def coinbase_exchange():
    exchange = ccxt.coinbase(coinbase_settings)
    return CCXTPandasExchange(exchange=exchange)


@pytest.fixture(scope="module")
def binance_exchange():
    exchange = ccxt.binance({"options": {"loadAllOptions": True}})
    return CCXTPandasExchange(exchange=exchange)


@pytest.fixture(scope="module")
def binance_authenticated_exchange():
    exchange = ccxt.binance(settings)
    return CCXTPandasExchange(exchange=exchange)


@pytest.fixture(scope="module")
def sandbox_exchange():
    exchange = ccxt.binance(sandbox_settings)
    exchange.set_sandbox_mode(True)
    return CCXTPandasExchange(exchange=exchange)


@pytest.fixture(scope="module")
def okx_exchange():
    exchange = ccxt.okx()
    exchange.set_sandbox_mode(True)
    return CCXTPandasExchange(exchange=exchange)


@pytest.fixture(scope="module")
def okx_authenticated_exchange():
    exchange = ccxt.okx(okx_settings)
    exchange.set_sandbox_mode(True)
    return CCXTPandasExchange(exchange=exchange)


@pytest.fixture(scope="module")
def gate_exchange():
    return CCXTPandasExchange(exchange=ccxt.gate())


@pytest.fixture(scope="module")
def bybit_exchange():
    return CCXTPandasExchange(exchange=ccxt.bybit())


def test_load_markets(sandbox_exchange):
    data = sandbox_exchange.load_markets()
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_balance(binance_authenticated_exchange):
    data = binance_authenticated_exchange.fetch_balance()
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_accounts(okx_authenticated_exchange):
    data = okx_authenticated_exchange.fetch_accounts()
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_portfolios(coinbase_exchange):
    data = coinbase_exchange.fetch_portfolios()
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)
    data = coinbase_exchange.fetch_portfolio_details(portfolioUuid=data["id"][0])
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_trading_fee(binance_authenticated_exchange):
    data = binance_authenticated_exchange.fetch_trading_fee(symbol=spot_symbol_list)
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_trading_fees(binance_authenticated_exchange):
    data = binance_authenticated_exchange.fetch_trading_fees()
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


# def test_fetch_transaction_fees(okx_authenticated_exchange):
#     data = okx_authenticated_exchange.fetch_transaction_fees()
#     print(data)
#     print(data.dtypes)
#     assert isinstance(data, pd.DataFrame)


def test_fetch_transfers(binance_authenticated_exchange):
    data = binance_authenticated_exchange.fetch_transfers()
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_currencies(binance_authenticated_exchange):
    data = binance_authenticated_exchange.fetch_currencies()
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_deposit_withdraw_fees(binance_authenticated_exchange):
    data = binance_authenticated_exchange.fetch_deposit_withdraw_fees()
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_deposits(binance_authenticated_exchange):
    data = binance_authenticated_exchange.fetch_deposits()
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_withdrawals(binance_authenticated_exchange):
    data = binance_authenticated_exchange.fetch_withdrawals()
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_deposit_addresses(coinbase_exchange):
    data = coinbase_exchange.fetch_deposit_addresses()
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


# def test_fetch_deposits_withdrawals(coinbase_exchange):
#     data = coinbase_exchange.fetch_deposits_withdrawals()
#     print(data)
#     print(data.dtypes)
#     assert isinstance(data, pd.DataFrame)


def test_fetch_ticker(sandbox_exchange):
    data = sandbox_exchange.fetch_ticker(symbol=spot_symbol_list)
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_tickers(sandbox_exchange):
    data = sandbox_exchange.fetch_tickers(symbols=spot_symbol_list)
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_order_book(sandbox_exchange):
    data = sandbox_exchange.fetch_order_book(symbol=spot_symbol)
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_ohlcv(sandbox_exchange):
    data = sandbox_exchange.fetch_ohlcv(symbol=spot_symbol)
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_status(binance_exchange):
    data = binance_exchange.fetch_status()
    print(data)
    assert isinstance(data, dict)


def test_fetch_trades(sandbox_exchange):
    data = sandbox_exchange.fetch_trades(symbol=spot_symbol)
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_my_trades(sandbox_exchange):
    data = sandbox_exchange.fetch_my_trades(symbol=spot_symbol)
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_mark_price(sandbox_exchange):
    data = sandbox_exchange.fetch_mark_price(symbol=spot_symbol_list)
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_mark_prices(sandbox_exchange):
    data = sandbox_exchange.fetch_mark_prices()
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_markets(sandbox_exchange):
    data = sandbox_exchange.fetch_markets()
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_cross_borrow_rates(okx_authenticated_exchange):
    data = okx_authenticated_exchange.fetch_cross_borrow_rates()
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_borrow_interest(okx_authenticated_exchange):
    data = okx_authenticated_exchange.fetch_borrow_interest()
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_isolated_borrow_rates(binance_authenticated_exchange):
    data = binance_authenticated_exchange.fetch_isolated_borrow_rates()
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_orders(sandbox_exchange):
    data = sandbox_exchange.fetch_orders(symbol=spot_symbol)
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_open_orders(sandbox_exchange):
    data = sandbox_exchange.fetch_open_orders(symbol=spot_symbol)
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_closed_orders(sandbox_exchange):
    data = sandbox_exchange.fetch_closed_orders(symbol=spot_symbol)
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_greeks(binance_exchange):
    options_symbol = (
        binance_exchange.load_markets()
        .query("type == 'option'")
        .head(3)["symbol"]
        .tolist()
    )
    print(options_symbol)
    data = binance_exchange.fetch_greeks(symbol=options_symbol)
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_option_chain(bybit_exchange):
    data = bybit_exchange.fetch_option_chain(code=["BTC", "ETH"])
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_all_greeks(binance_exchange):
    data = binance_exchange.fetch_all_greeks()
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_position(binance_authenticated_exchange):
    options_symbol = (
        binance_authenticated_exchange.load_markets()
        .query("type == 'option'")
        .head(3)["symbol"]
        .tolist()
    )
    print(options_symbol)
    data = binance_authenticated_exchange.fetch_position(symbol=options_symbol)
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_positions(binance_authenticated_exchange):
    data = binance_authenticated_exchange.fetch_positions()
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_positions_adl_rank(binance_authenticated_exchange):
    data = binance_authenticated_exchange.fetch_positions_adl_rank()
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_option_positions(binance_authenticated_exchange):
    data = binance_authenticated_exchange.fetch_option_positions()
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_ledger(binance_authenticated_exchange):
    data = binance_authenticated_exchange.fetch_ledger()
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_withdrawals(binance_authenticated_exchange):
    data = binance_authenticated_exchange.fetch_withdrawals(
        code=["BTC", "ETH", "BNB", "DOGE"]
    )
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_funding_rate_history(binance_exchange):
    data = binance_exchange.fetch_funding_rate_history(symbol="BNB/USDT:USDT")
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_last_prices(binance_exchange):
    data = binance_exchange.fetch_last_prices(symbols=spot_symbol_list)
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_open_interest(binance_exchange):
    data = binance_exchange.fetch_open_interest(symbol=swap_symbol_list)
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_open_interest_history(binance_exchange):
    data = binance_exchange.fetch_open_interest_history(symbol=swap_symbol_list)
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_liquidations(gate_exchange):
    data = gate_exchange.fetch_liquidations(symbol=swap_symbol_list)
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_leverages(binance_authenticated_exchange):
    data = binance_authenticated_exchange.fetch_leverages(symbols=swap_symbol_list)
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_long_short_ratio_history(binance_exchange):
    data = binance_exchange.fetch_long_short_ratio_history(symbol=swap_symbol_list)
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_margin_adjustment_history(binance_authenticated_exchange):
    data = binance_authenticated_exchange.fetch_margin_adjustment_history(
        symbol=swap_symbol_list
    )
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_my_liquidations(binance_authenticated_exchange):
    data = binance_authenticated_exchange.fetch_my_liquidations(symbol=swap_symbol_list)
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


# def test_fetch_option(exchange):
#     data = exchange.fetch_option(symbol)
#     print(data)
#     assert isinstance(data, dict)


def test_fetch_funding_rates(sandbox_exchange):
    data = sandbox_exchange.fetch_funding_rates(symbols=swap_symbol_list)
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_convert_trade_history(binance_authenticated_exchange):
    data = binance_authenticated_exchange.fetch_convert_trade_history()
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_bids_asks(sandbox_exchange):
    data = sandbox_exchange.fetch_bids_asks(symbols=swap_symbol_list)
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_canceled_and_closed_orders(sandbox_exchange):
    data = sandbox_exchange.fetch_canceled_and_closed_orders(symbol=spot_symbol)
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_convert_currencies(binance_authenticated_exchange):
    data = binance_authenticated_exchange.fetch_convert_currencies()
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_cross_borrow_rate(binance_authenticated_exchange):
    data = binance_authenticated_exchange.fetch_cross_borrow_rate(code="BTC")
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_funding_interval(okx_exchange):
    data = okx_exchange.fetch_funding_interval(
        symbol=["BTC/USDT:USDT", "ETH/USDT:USDT"]
    )
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_open_interests(okx_exchange):
    data = okx_exchange.fetch_open_interests()
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_fetch_funding_intervals(binance_exchange):
    data = binance_exchange.fetch_funding_intervals()
    print(data)
    print(data.dtypes)
    assert isinstance(data, pd.DataFrame)


def test_create_order(okx_authenticated_exchange):
    data = okx_authenticated_exchange.create_order(
        symbol=spot_symbol,
        type="limit",
        side="buy",
        amount=0.01,
        price=500.0,
    )
    print(data)
    assert isinstance(data, dict)
    data = okx_authenticated_exchange.fetch_order(id=data["id"], symbol=spot_symbol)
    print(data)
    assert isinstance(data, pd.DataFrame)
    data = okx_authenticated_exchange.cancel_order(
        id=data["id"].values[0], symbol=spot_symbol
    )
    print(data)
    assert isinstance(data, pd.DataFrame)


def test_create_orders(okx_authenticated_exchange):
    orders = [
        dict(
            side="buy",
            price=300.0,
        ),
        dict(
            side="sell",
            price=6000,
        ),
    ]
    orders = pd.DataFrame(orders)
    orders["cost"] = 7
    orders["type"] = "limit"
    orders["symbol"] = spot_symbol
    data = okx_authenticated_exchange.create_orders_from_dataframe(orders=orders)
    print(data)
    assert isinstance(data, pd.DataFrame)
    data = okx_authenticated_exchange.fetch_open_orders(symbol=spot_symbol)
    print(data)
    assert isinstance(data, pd.DataFrame)
    if not data.empty:
        data["amount"] *= 2
        data = okx_authenticated_exchange.edit_orders_from_dataframe(orders=data)
        print(data)
        assert isinstance(data, pd.DataFrame)
        data = okx_authenticated_exchange.cancel_all_orders(symbol=spot_symbol)
        print(data)
        assert isinstance(data, pd.DataFrame)
