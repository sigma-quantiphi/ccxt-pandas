"""Delta hedging calculations for portfolio management."""

from typing import Literal, Union

import pandas as pd
import pandera as pa
from pandera.typing import DataFrame

from ccxt_pandas.wrappers.schemas.balance_schema import BalanceSchema
from ccxt_pandas.wrappers.schemas.margins_balance_schema import MarginsBalanceSchema
from ccxt_pandas.wrappers.schemas.market_schema import MarketSchema
from ccxt_pandas.wrappers.schemas.positions_schema import PositionsSchema


@pa.check_types
def calculate_delta_exposure(
    balance: Union[DataFrame[BalanceSchema], DataFrame[MarginsBalanceSchema]],
    positions: DataFrame[PositionsSchema],
    markets: DataFrame[MarketSchema],
    balance_amount: Literal["free", "used", "total"] = "total",
    amount_column: str = "amount",
) -> pd.DataFrame:
    """Calculate net delta exposure across spot, swap, and futures positions.

    This function combines spot balances with derivatives positions to calculate
    the total exposure in each base currency, useful for delta hedging strategies.

    Supports both spot balances (BalanceSchema) and margin balances (MarginsBalanceSchema).

    Args:
        balance: Balance DataFrame from fetch_balance. Can be either:
            - BalanceSchema: Spot balances with 'code', 'free', 'used', 'total' columns
            - MarginsBalanceSchema: Margin balances with 'symbol', 'base', 'base_free',
              'base_used', 'base_total' columns
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

        >>> # Spot balances
        >>> balance = exchange.fetch_balance()
        >>> positions = exchange.fetch_positions()
        >>> markets = exchange.load_markets()
        >>> delta = calculate_delta_exposure(balance, positions, markets)
        >>> print(delta)
           base    amount
        0  BTC   1.234567
        1  ETH  12.345678
        2  USDT  1000.00

        >>> # Margin balances (also supported)
        >>> margin_balance = exchange.fetch_balance()  # In margin mode
        >>> delta = calculate_delta_exposure(margin_balance, positions, markets)

    Raises:
        pandera.errors.SchemaError: If any DataFrame doesn't match its schema
            - balance must match BalanceSchema or MarginsBalanceSchema
            - positions must match PositionsSchema
            - markets must match MarketSchema

    Notes:
        - For positions, 'long' side is treated as positive exposure
        - For positions, 'short' side is treated as negative exposure
        - Amounts are converted using contractSize for derivatives
        - Spot balances: uses 'code' column (currency code) renamed to 'base'
        - Margin balances: uses 'base' column directly and 'base_*' amount columns
        - Automatically detects balance type based on columns present
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

    # Prepare balance DataFrame - handle both spot and margin balances
    balance_calc = balance.copy()

    # Detect balance type and prepare accordingly
    if "code" in balance_calc.columns:
        # BalanceSchema (spot balances)
        # Rename: code -> base, {balance_amount} -> amount_column
        balance_calc = balance_calc.rename(
            columns={"code": "base", balance_amount: amount_column}
        )[["base", amount_column]]
    elif "symbol" in balance_calc.columns:
        # MarginsBalanceSchema (margin balances)
        # Use 'base' column directly, select base_{balance_amount} -> amount_column
        margin_amount_col = f"base_{balance_amount}"
        balance_calc = balance_calc.rename(columns={margin_amount_col: amount_column})[
            ["base", amount_column]
        ]
    else:
        raise ValueError(
            "Balance DataFrame must have either 'code' column (BalanceSchema) "
            "or 'symbol' column (MarginsBalanceSchema)"
        )

    # Select only base and amount columns from positions
    positions_for_concat = positions_calc[["base", amount_column]]

    # Concatenate and sum by base currency
    delta = (
        pd.concat([balance_calc, positions_for_concat], ignore_index=True)
        .groupby("base", as_index=False)[amount_column]
        .sum()
    )

    return delta
