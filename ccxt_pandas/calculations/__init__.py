"""Calculation utilities for ccxt-pandas.

This package provides higher-level calculation functions for common trading
and risk management tasks, built on top of the ccxt-pandas DataFrame outputs.
"""

from ccxt_pandas.calculations.delta import calculate_delta_exposure
from ccxt_pandas.calculations.precision import ceil_series, floor_series
from ccxt_pandas.calculations.trades import (
    aggregate_trades,
    calculate_realized_pnl,
)
from ccxt_pandas.calculations.orderbook import (
    calculate_mid_price,
    calculate_notional,
    calculate_spread,
    calculate_vwap_by_depth,
    create_mirrored_sides,
    is_ask_side,
    side_sign,
    signed_price,
    sort_orderbook,
)

__all__ = [
    "calculate_delta_exposure",
    "aggregate_trades",
    "calculate_realized_pnl",
    "floor_series",
    "ceil_series",
    "calculate_mid_price",
    "calculate_notional",
    "calculate_spread",
    "calculate_vwap_by_depth",
    "create_mirrored_sides",
    "is_ask_side",
    "side_sign",
    "signed_price",
    "sort_orderbook",
]
