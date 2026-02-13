"""Calculation utilities for ccxt-pandas.

This package provides higher-level calculation functions for common trading
and risk management tasks, built on top of the ccxt-pandas DataFrame outputs.
"""

from ccxt_pandas.calculations.delta import calculate_delta_exposure
from ccxt_pandas.calculations.trades import (
    aggregate_trades,
    calculate_realized_pnl,
)

__all__ = [
    "calculate_delta_exposure",
    "aggregate_trades",
    "calculate_realized_pnl",
]
