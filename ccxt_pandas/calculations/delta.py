"""Delta hedging calculations for portfolio management."""

from typing import Literal, Optional

import pandas as pd
import pandera as pa
from pandera.typing import DataFrame

from ccxt_pandas.wrappers.schemas.balance_schema import BalanceSchema
from ccxt_pandas.wrappers.schemas.market_schema import MarketSchema
from ccxt_pandas.wrappers.schemas.positions_schema import PositionsSchema


@pa.check_types
def calculate_delta_exposure(
    balance: DataFrame[BalanceSchema],
    positions: DataFrame[PositionsSchema],
    markets: DataFrame[MarketSchema],
    balance_amount: Literal["free", "used", "total"] = "total",
    amount_column: str = "amount",
) -> pd.DataFrame:
    """Calculate net delta exposure across spot, swap, and futures positions.

    This function combines spot balances with derivatives positions to calculate
    the total exposure in each base currency, useful for delta hedging strategies.

    Args:
        balance: Balance DataFrame from fetch_balance (must have 'code' column and
            balance amount columns: 'free', 'used', 'total').
        positions: Positions DataFrame from fetch_positions (must have 'symbol', 'contracts',
            'contractSize', and 'side' columns).
        markets: Markets DataFrame from load_markets (must have 'symbol' and 'base' columns).
        balance_amount: Which balance amount to use - 'free', 'used', or 'total' (default: 'total').
        amount_column: Output column name for amount/quantity (default: 'amount').

    Returns:
        DataFrame with columns: ['base', amount_column]
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

    Raises:
        pandera.errors.SchemaError: If any DataFrame doesn't match its schema
            - balance must match BalanceSchema
            - positions must match PositionsSchema
            - markets must match MarketSchema

    Notes:
        - For positions, 'long' side is treated as positive exposure
        - For positions, 'short' side is treated as negative exposure
        - Amounts are converted using contractSize for derivatives
        - Balance uses 'code' column (currency code) which is renamed to 'base'
        - Input validation performed via Pandera schemas
    """
    # Prepare positions with amounts
    positions_calc = positions.merge(
        markets[["symbol", "base"]], on="symbol", how="left"
    )

    # Calculate signed amount based on side (long = positive, short = negative)
    positions_calc[amount_column] = positions_calc["contracts"].where(
        positions_calc["side"] == "long", other=-positions_calc["contracts"]
    )
    positions_calc[amount_column] *= positions_calc["contractSize"]

    # Prepare balance DataFrame - rename code to base and select balance amount
    balance_calc = balance.copy()
    balance_calc = balance_calc.rename(
        columns={"code": "base", balance_amount: amount_column}
    )[["base", amount_column]]

    # Select only base and amount columns from positions
    positions_for_concat = positions_calc[["base", amount_column]]

    # Concatenate and sum by base currency
    delta = (
        pd.concat([balance_calc, positions_for_concat], ignore_index=True)
        .groupby("base", as_index=False)[amount_column]
        .sum()
    )

    return delta
