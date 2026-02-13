"""Delta hedging calculations for portfolio management."""

from typing import Optional

import pandas as pd


def calculate_delta_exposure(
    balance: pd.DataFrame,
    positions: pd.DataFrame,
    markets: pd.DataFrame,
    base_column: str = "base",
    code_column: str = "code",
    amount_column: str = "amount",
) -> pd.DataFrame:
    """Calculate net delta exposure across spot, swap, and futures positions.

    This function combines spot balances with derivatives positions to calculate
    the total exposure in each base currency, useful for delta hedging strategies.

    Args:
        balance: Balance DataFrame from fetch_balance (must have 'code' and 'amount' columns).
            For spot balances, use 'code' column. For margin balances, ensure 'base' is present.
        positions: Positions DataFrame from fetch_positions (must have 'symbol', 'contracts',
            'contractSize', and 'side' columns).
        markets: Markets DataFrame from load_markets (must have 'symbol' and 'base' columns).
        base_column: Column name for base currency (default: 'base').
        code_column: Column name for currency code in balance (default: 'code').
        amount_column: Column name for amount/quantity (default: 'amount').

    Returns:
        DataFrame with columns: [base_column, amount_column]
        showing net exposure in each base currency.

    Example:
        >>> import ccxt_pandas as cpd
        >>> exchange = cpd.CCXTPandasExchange(ccxt.binance())
        >>> balance = exchange.fetch_balance()
        >>> positions = exchange.fetch_positions()
        >>> markets = exchange.load_markets()
        >>> delta = calculate_delta_exposure(balance, positions, markets)
        >>> print(delta)
           base    amount
        0  BTC   1.234567
        1  ETH  12.345678
        2  USDT  1000.00

    Notes:
        - For positions, 'long' side is treated as positive exposure
        - For positions, 'short' side is treated as negative exposure
        - Amounts are converted using contractSize for derivatives
        - Balance must have either 'base' column (margin) or 'code' column (spot)
    """
    # Prepare positions with amounts
    positions_calc = positions.merge(
        markets[[\"symbol\", base_column]], on=\"symbol\", how=\"left\"
    )

    # Calculate signed amount based on side (long = positive, short = negative)
    positions_calc[amount_column] = positions_calc[\"contracts\"].where(
        positions_calc[\"side\"] == \"long\", other=-positions_calc[\"contracts\"]
    )
    positions_calc[amount_column] *= positions_calc[\"contractSize\"]

    # Prepare balance DataFrame
    # If balance has 'code' column (spot), rename to 'base' for consistency
    balance_calc = balance.copy()
    if code_column in balance_calc.columns and base_column not in balance_calc.columns:
        balance_calc = balance_calc.rename(columns={code_column: base_column})

    # Select only base and amount columns for concatenation
    positions_for_concat = positions_calc[[base_column, amount_column]]
    balance_for_concat = balance_calc[[base_column, amount_column]]

    # Concatenate and sum by base currency
    delta = (
        pd.concat([balance_for_concat, positions_for_concat], ignore_index=True)
        .groupby(base_column, as_index=False)[amount_column]
        .sum()
    )

    return delta
