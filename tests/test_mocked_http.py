"""Mock-HTTP unit tests demonstrating the `responses` fixture wiring.

These exercise the full DataFrame-conversion pipeline with stubbed HTTP
responses — no live exchange calls. They prove the conftest fixtures work
end-to-end and serve as a template for future endpoint coverage.
"""

from __future__ import annotations

import responses


def _stub_market(symbol: str, base: str, quote: str, market_id: str) -> dict:
    """Minimal market dict with all type flags ccxt internals expect."""
    return {
        "symbol": symbol,
        "base": base,
        "quote": quote,
        "id": market_id,
        "type": "spot",
        "spot": True,
        "margin": False,
        "swap": False,
        "future": False,
        "option": False,
        "contract": False,
        "linear": None,
        "inverse": None,
        "settle": None,
        "settleId": None,
        "active": True,
        "precision": {"price": 0.01, "amount": 0.00001},
        "limits": {
            "amount": {"min": 0.00001, "max": None},
            "price": {"min": 0.01, "max": None},
            "cost": {"min": 5.0, "max": None},
        },
        "info": {},
    }


@responses.activate
def test_fetch_ohlcv_returns_typed_dataframe(binance_unauth):
    """Stubbed klines response → DataFrame with UTC timestamp + numeric OHLCV."""
    # Pre-populate markets so fetch_ohlcv doesn't call load_markets first.
    binance_unauth.exchange.markets = {
        "BTC/USDT": _stub_market("BTC/USDT", "BTC", "USDT", "BTCUSDT"),
    }
    binance_unauth.exchange.markets_by_id = {
        "BTCUSDT": [binance_unauth.exchange.markets["BTC/USDT"]]
    }

    # Each kline row: [openTime, open, high, low, close, volume, closeTime, quoteVol, trades, ...]
    responses.add(
        responses.GET,
        "https://api.binance.com/api/v3/klines",
        json=[
            [
                1712188800000,
                "70000.0",
                "70100.0",
                "69950.0",
                "70050.0",
                "12.5",
                1712188859999,
                "875625.0",
                100,
                "6.0",
                "420300.0",
                "0",
            ],
            [
                1712188860000,
                "70050.0",
                "70200.0",
                "70000.0",
                "70150.0",
                "15.0",
                1712188919999,
                "1052250.0",
                120,
                "7.5",
                "525825.0",
                "0",
            ],
        ],
        status=200,
    )

    df = binance_unauth.fetch_ohlcv(symbol="BTC/USDT", timeframe="1m", limit=2)

    assert len(df) == 2
    assert {"timestamp", "open", "high", "low", "close", "volume"}.issubset(df.columns)
    assert df["timestamp"].dtype.kind == "M"  # datetime64
    assert df["open"].iloc[0] == 70000.0
    assert df["close"].iloc[1] == 70150.0


@responses.activate
def test_fetch_order_book_returns_levels_dataframe(binance_unauth):
    """Stubbed depth response → DataFrame with bid/ask side rows."""
    binance_unauth.exchange.markets = {
        "BTC/USDT": _stub_market("BTC/USDT", "BTC", "USDT", "BTCUSDT"),
    }
    binance_unauth.exchange.markets_by_id = {
        "BTCUSDT": [binance_unauth.exchange.markets["BTC/USDT"]]
    }

    responses.add(
        responses.GET,
        "https://api.binance.com/api/v3/depth",
        json={
            "lastUpdateId": 1,
            "bids": [["70000.00", "1.5"], ["69950.00", "2.0"]],
            "asks": [["70050.00", "1.0"], ["70100.00", "3.5"]],
        },
        status=200,
    )

    df = binance_unauth.fetch_order_book(symbol="BTC/USDT", limit=10)

    assert len(df) == 4  # 2 bids + 2 asks
    assert set(df["side"]) == {"bids", "asks"}
    assert df["price"].dtype.kind == "f"  # numeric
    assert df["qty"].dtype.kind == "f"
