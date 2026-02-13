"""Precision and rounding utilities for numerical data."""

import numpy as np
import pandas as pd


def floor_series(data: pd.Series, digits: int = 0) -> pd.Series:
    """Round Series values down to specified decimal places.

    Args:
        data: Series to round
        digits: Number of decimal places (default: 0)

    Returns:
        Series with values rounded down

    Examples:
        >>> prices = pd.Series([1.2345, 2.6789, 3.9999])
        >>> floor_series(prices, digits=2)
        0    1.23
        1    2.67
        2    3.99
        dtype: float64

        >>> # Round to nearest integer (floor)
        >>> floor_series(prices)
        0    1.0
        1    2.0
        2    3.0
        dtype: float64

    Notes:
        - Uses numpy floor to round down
        - Useful for price/amount precision requirements
        - For rounding up, use ceil_series()
    """
    return pd.Series(np.floor(data * 10**digits) / 10**digits)


def ceil_series(data: pd.Series, digits: int = 0) -> pd.Series:
    """Round Series values up to specified decimal places.

    Args:
        data: Series to round
        digits: Number of decimal places (default: 0)

    Returns:
        Series with values rounded up

    Examples:
        >>> prices = pd.Series([1.2345, 2.6789, 3.0001])
        >>> ceil_series(prices, digits=2)
        0    1.24
        1    2.68
        2    3.01
        dtype: float64

        >>> # Round to nearest integer (ceil)
        >>> ceil_series(prices)
        0    2.0
        1    3.0
        2    4.0
        dtype: float64

    Notes:
        - Uses numpy ceil to round up
        - Useful for minimum order size requirements
        - For rounding down, use floor_series()
    """
    return pd.Series(np.ceil(data * 10**digits) / 10**digits)
