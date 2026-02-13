"""Calculation utilities for ccxt-pandas.

This package provides higher-level calculation functions for common trading
and risk management tasks, built on top of the ccxt-pandas DataFrame outputs.
"""

from ccxt_pandas.calculations.delta import calculate_delta_exposure

__all__ = ["calculate_delta_exposure"]
