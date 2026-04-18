"""Trade analysis and PnL calculation utilities."""

import numpy as np
import pandas as pd
import pandera as pa
from pandera.typing import DataFrame

from ccxt_pandas.wrappers.schemas.trade_schema import MyTradesSchema


@pa.check_types
def aggregate_trades(
    trades: DataFrame[MyTradesSchema],
    group_by: list[str] | tuple = ("symbol", "side"),
    freq: str | None = None,
    include_fees: bool = True,
) -> pd.DataFrame:
    """Aggregate trades by specified columns with optional time resampling.

    Groups trades and calculates total amounts, costs, fees, and trade counts.
    Useful for summarizing trading activity across symbols, sides, or time periods.

    Args:
        trades: Trades DataFrame from fetch_my_trades() with required columns:
            - symbol: Trading pair
            - side: 'buy' or 'sell'
            - amount: Trade amount
            - cost: Trade cost/value
            - timestamp: Trade timestamp (required if freq is provided)
            - fee_cost: Fee amount (optional, required if include_fees=True)
        group_by: Columns to group by. Default: ("symbol", "side")
        freq: Optional pandas frequency string for time aggregation
            (e.g., "1H", "1D", "1W"). If provided, groups by timestamp.
        include_fees: Whether to include fee_cost in aggregation. Default: True

    Returns:
        Aggregated DataFrame with columns:
            - {group_by columns}: Grouping columns
            - amount: Total amount traded
            - cost: Total cost/value
            - n_trades: Number of trades
            - fee_cost: Total fees (if include_fees=True and fee_cost exists)
            - signed_amount: Amount with buy=+, sell=-
            - signed_cost: Cost with buy=+, sell=-

    Examples:
        >>> # Aggregate by symbol and side
        >>> summary = aggregate_trades(trades)
        >>> print(summary)
           symbol  side  amount    cost  n_trades  fee_cost  signed_amount  signed_cost
        0  BTC/USDT  buy   1.5   45000        10      45.0           1.5        45000.0
        1  BTC/USDT  sell  1.0   31000         5      31.0          -1.0       -31000.0

        >>> # Aggregate by symbol only (combines buy/sell)
        >>> summary = aggregate_trades(trades, group_by=["symbol"])

        >>> # Aggregate by hour
        >>> hourly = aggregate_trades(trades, freq="1H")

    Raises:
        pandera.errors.SchemaError: If trades DataFrame doesn't match MyTradesSchema

    Notes:
        - If trades is empty, returns empty DataFrame with correct columns
        - signed_amount: positive for buys, negative for sells
        - signed_cost: positive for buys, negative for sells
        - If 'side' is in group_by, it's converted to Categorical for proper ordering
        - Input validation performed via Pandera MyTradesSchema
    """
    # Handle empty DataFrame
    if trades.empty:
        result_columns = list(group_by) + [
            "amount",
            "cost",
            "n_trades",
            "signed_amount",
            "signed_cost",
        ]
        if include_fees and "fee_cost" in trades.columns:
            result_columns.insert(3, "fee_cost")
        return pd.DataFrame(columns=result_columns)

    # Create working copy
    result = trades.copy()

    # Build index for grouping
    index = list(group_by)

    # Add trade counter
    result["n_trades"] = 1

    # Handle time-based aggregation
    if freq:
        if "timestamp" not in index:
            index.append("timestamp")
        result["timestamp"] = result["timestamp"].dt.floor(freq)

    # Convert side to categorical for proper ordering
    if "side" in group_by:
        result["side"] = pd.Categorical(result["side"], categories=["buy", "sell"])

    # Calculate signed amounts and costs
    result["signed_amount"] = result["amount"].where(
        result["side"] == "buy", other=-result["amount"]
    )
    result["signed_cost"] = result["cost"].where(result["side"] == "buy", other=-result["cost"])

    # Define columns to aggregate
    agg_columns = ["amount", "cost", "n_trades", "signed_amount", "signed_cost"]
    if include_fees and "fee_cost" in result.columns:
        agg_columns.insert(2, "fee_cost")

    # Group and aggregate
    result = result.groupby(by=index, as_index=False)[agg_columns].sum()

    return result


@pa.check_types
def calculate_realized_pnl(
    trades: DataFrame[MyTradesSchema],
    group_by: list[str] | tuple = ("symbol",),
    freq: str | None = None,
    include_totals: bool = False,
) -> pd.DataFrame:
    """Calculate realized PnL metrics by matching buy and sell trades.

    Pivots trades by side (buy/sell) and calculates:
    - Average buy/sell prices
    - Price spread
    - Matched amounts (trades that entered and exited)
    - Net position (unmatched trades)
    - Realized PnL from matched trades

    Args:
        trades: Trades DataFrame from fetch_my_trades() with required columns:
            - symbol: Trading pair
            - side: 'buy' or 'sell'
            - amount: Trade amount
            - cost: Trade cost/value
            - timestamp: Trade timestamp (required if freq is provided)
            - fee_cost: Fee amount (optional)
        group_by: Columns to group by. Default: ("symbol",)
        freq: Optional pandas frequency string for time aggregation
            (e.g., "1H", "1D", "1W"). If provided, groups by timestamp.
        include_totals: Whether to include "All" totals row. Default: False

    Returns:
        DataFrame with columns:
            - {group_by columns}: Grouping columns
            - amount_buy, amount_sell: Total amounts per side
            - cost_buy, cost_sell: Total costs per side
            - n_trades_buy, n_trades_sell: Trade counts per side
            - fee_cost_buy, fee_cost_sell: Fees per side (if fee_cost exists)
            - price_buy, price_sell: Average prices (cost/amount)
            - spread: Price difference (sell - buy)
            - amount_in_out: Matched amount (min of buy/sell)
            - amount_net: Net position (buy - sell)
            - pnl_in_out: Realized PnL (matched_amount * spread)

    Examples:
        >>> # Calculate PnL per symbol
        >>> pnl = calculate_realized_pnl(trades)
        >>> print(pnl)
           symbol  amount_buy  amount_sell  price_buy  price_sell  spread  amount_in_out  amount_net  pnl_in_out
        0  BTC/USDT        1.5          1.0    30000.0     31000.0  1000.0            1.0         0.5      1000.0

        >>> # Calculate daily PnL
        >>> daily_pnl = calculate_realized_pnl(trades, freq="1D")

        >>> # PnL with totals row
        >>> pnl = calculate_realized_pnl(trades, include_totals=True)

    Raises:
        pandera.errors.SchemaError: If trades DataFrame doesn't match MyTradesSchema

    Notes:
        - Only calculates PnL for trades that have both buys and sells
        - Net position shows unmatched trades (inventory)
        - Fees are not included in PnL calculation (shown separately)
        - Price calculations handle division by zero (returns 0)
        - If trades is empty, returns empty DataFrame with correct columns
        - Input validation performed via Pandera MyTradesSchema
    """
    # Handle empty DataFrame
    if trades.empty:
        base_columns = list(group_by) + [
            "amount_buy",
            "amount_sell",
            "cost_buy",
            "cost_sell",
            "n_trades_buy",
            "n_trades_sell",
        ]
        if "fee_cost" in trades.columns:
            base_columns.extend(["fee_cost_buy", "fee_cost_sell"])
        base_columns.extend(
            [
                "price_buy",
                "price_sell",
                "spread",
                "amount_in_out",
                "amount_net",
                "pnl_in_out",
            ]
        )
        return pd.DataFrame(columns=base_columns)

    # Create working copy
    result = trades.copy()

    # Build index for grouping
    index = list(group_by)

    # Add trade counter
    result["n_trades"] = 1

    # Handle time-based aggregation
    if freq:
        if "timestamp" not in index:
            index.append("timestamp")
        result["timestamp"] = result["timestamp"].dt.floor(freq)

    # Convert side to categorical for proper ordering
    result["side"] = pd.Categorical(result["side"], categories=["buy", "sell"])

    # Define values to pivot
    values = ["amount", "cost", "n_trades"]
    if "fee_cost" in result.columns:
        values.append("fee_cost")

    # Pivot table by side
    result = result.pivot_table(
        index=index,
        columns="side",
        values=values,
        aggfunc="sum",
        margins=include_totals,
        margins_name="All",
        observed=False,
    )

    # Remove totals row if not requested
    if not include_totals and "All" in result.index:
        result = result.drop("All", axis=0)

    # Flatten column names
    result.columns = ["_".join([str(x) for x in col if x != ""]) for col in result.columns]

    # Reset index to make grouping columns regular columns
    result = result.reset_index()

    # Fill NaN with 0
    result = result.fillna(0)

    # Calculate average prices (handle division by zero)
    result["price_buy"] = np.where(
        result["amount_buy"] != 0, result["cost_buy"] / result["amount_buy"], 0
    )
    result["price_sell"] = np.where(
        result["amount_sell"] != 0, result["cost_sell"] / result["amount_sell"], 0
    )

    # Calculate spread
    result["spread"] = result["price_sell"] - result["price_buy"]

    # Calculate matched amounts and net position
    result["amount_in_out"] = result[["amount_buy", "amount_sell"]].min(axis=1)
    result["amount_net"] = result["amount_buy"] - result["amount_sell"]

    # Calculate realized PnL from matched trades
    result["pnl_in_out"] = result["amount_in_out"] * result["spread"]

    return result
