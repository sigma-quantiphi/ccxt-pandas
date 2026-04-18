"""Pure-pandas unit tests for the calculations module.

These don't hit any exchange — they exercise the DataFrame helpers directly
with hand-crafted frames.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from ccxt_pandas import (
    calculate_mid_price_and_spread,
    calculate_notional,
    calculate_vwap_by_depth,
    ceil_series,
    create_mirrored_sides,
    floor_series,
    is_ask_side,
    side_sign,
    signed_price,
    sort_orderbook,
)


def test_floor_series_default_digits():
    s = pd.Series([1.2345, 2.6789, 3.9999])
    pd.testing.assert_series_equal(floor_series(s), pd.Series([1.0, 2.0, 3.0]))


def test_floor_series_with_digits():
    s = pd.Series([1.2345, 2.6789, 3.9999])
    pd.testing.assert_series_equal(floor_series(s, digits=2), pd.Series([1.23, 2.67, 3.99]))


def test_ceil_series_default_digits():
    s = pd.Series([1.2345, 2.6789, 3.0001])
    pd.testing.assert_series_equal(ceil_series(s), pd.Series([2.0, 3.0, 4.0]))


def test_ceil_series_with_digits():
    s = pd.Series([1.2345, 2.6789, 3.0001])
    pd.testing.assert_series_equal(ceil_series(s, digits=2), pd.Series([1.24, 2.68, 3.01]))


def test_is_ask_side_orderbook_format():
    df = pd.DataFrame({"side": ["bids", "asks", "bids"]})
    pd.testing.assert_series_equal(
        is_ask_side(df), pd.Series([False, True, False]), check_names=False
    )


def test_is_ask_side_order_format():
    df = pd.DataFrame({"side": ["buy", "sell", "buy"]})
    pd.testing.assert_series_equal(
        is_ask_side(df), pd.Series([False, True, False]), check_names=False
    )


def test_side_sign():
    df = pd.DataFrame({"side": ["bids", "asks", "buy", "sell"]})
    assert side_sign(df).tolist() == [-1, 1, -1, 1]


def test_signed_price():
    df = pd.DataFrame({"side": ["bids", "asks"], "price": [99.5, 100.5]})
    pd.testing.assert_series_equal(signed_price(df), pd.Series([-99.5, 100.5]), check_names=False)


def test_create_mirrored_sides():
    orders = pd.DataFrame({"price": [100, 101], "qty": [1.0, 2.0]})
    mirrored = create_mirrored_sides(orders)
    assert len(mirrored) == 4
    assert mirrored["side"].tolist() == ["buy", "buy", "sell", "sell"]


def test_sort_orderbook_puts_best_first():
    orderbook = pd.DataFrame(
        {
            "symbol": ["BTC/USDT"] * 4,
            "side": ["asks", "bids", "asks", "bids"],
            "price": [101.0, 99.0, 100.0, 98.0],
            "qty": [1.0, 2.0, 1.5, 1.0],
        }
    )
    sorted_ob = sort_orderbook(orderbook)
    bid_rows = sorted_ob[sorted_ob["side"] == "bids"]
    ask_rows = sorted_ob[sorted_ob["side"] == "asks"]
    # best bid first = highest price first
    assert bid_rows.iloc[0]["price"] == 99.0
    # best ask first = lowest price first
    assert ask_rows.iloc[0]["price"] == 100.0


def test_calculate_notional():
    df = pd.DataFrame({"price": [100.0, 101.0], "qty": [1.5, 2.0]})
    pd.testing.assert_series_equal(
        calculate_notional(df), pd.Series([150.0, 202.0]), check_names=False
    )


def test_calculate_mid_price_and_spread():
    orderbook = pd.DataFrame(
        {
            "symbol": ["BTC/USDT", "BTC/USDT", "ETH/USDT", "ETH/USDT"],
            "side": ["bids", "asks", "bids", "asks"],
            "price": [99.5, 100.5, 1800.0, 1820.0],
        }
    )
    out = calculate_mid_price_and_spread(orderbook)
    assert set(out.columns) == {"bid", "ask", "mid_price", "spread", "relative_spread"}
    assert out.loc["BTC/USDT", "mid_price"] == 100.0
    assert out.loc["BTC/USDT", "spread"] == 1.0
    assert out.loc["ETH/USDT", "mid_price"] == 1810.0
    assert out.loc["ETH/USDT", "spread"] == 20.0


def test_calculate_vwap_by_depth_partial_fill():
    # Buy $500 at 100 (5 qty out of 10 available) — VWAP should be exactly 100
    orderbook = pd.DataFrame(
        {
            "symbol": ["BTC/USDT"] * 4,
            "side": ["asks"] * 4,
            "price": [100.0, 101.0, 102.0, 103.0],
            "qty": [10.0, 10.0, 10.0, 10.0],
        }
    )
    vwap = calculate_vwap_by_depth(orderbook, depths=[500.0])
    row = vwap.iloc[0]
    assert row["depth"] == 500.0
    assert row["price"] == pytest.approx(100.0)
    assert row["notional"] == pytest.approx(500.0)


def test_calculate_vwap_by_depth_crosses_levels():
    # Buy $1500 at 100/101 — first 1000 at 100, next 500 at 101 → VWAP ≈ 100.33
    orderbook = pd.DataFrame(
        {
            "symbol": ["BTC/USDT"] * 4,
            "side": ["asks"] * 4,
            "price": [100.0, 101.0, 102.0, 103.0],
            "qty": [10.0, 10.0, 10.0, 10.0],
        }
    )
    vwap = calculate_vwap_by_depth(orderbook, depths=[1500.0])
    row = vwap.iloc[0]
    expected = 1500.0 / (1000.0 / 100.0 + 500.0 / 101.0)
    assert row["price"] == pytest.approx(expected, rel=1e-6)


def test_signed_price_alias_for_sort_keeps_best_at_top():
    """signed_price reverses bid order so sort ascending puts best bid first."""
    df = pd.DataFrame({"side": ["bids", "bids", "bids"], "price": [98.0, 99.0, 99.5]})
    sp = signed_price(df)
    # All bids → all negative; ascending sort puts most negative first = highest abs price = best bid
    assert sp.tolist() == [-98.0, -99.0, -99.5]
    assert np.argmin(sp) == 2  # index 2 (price 99.5) sorts first
