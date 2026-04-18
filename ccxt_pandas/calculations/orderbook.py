"""Order book analysis and depth calculations."""


import pandas as pd


def create_mirrored_sides(
    data: pd.DataFrame, sides: tuple[str, str] = ("buy", "sell")
) -> pd.DataFrame:
    """Create mirrored order book sides for testing or simulation.

    Takes a DataFrame and duplicates it for each side, useful for creating
    synthetic order books or testing strategies with symmetric orders.

    Args:
        data: DataFrame with order data (price, qty, etc.)
        sides: Tuple of side values to create (default: ("buy", "sell"))

    Returns:
        DataFrame with rows duplicated for each side

    Examples:
        >>> # Create buy and sell orders from a single set
        >>> orders = pd.DataFrame({'price': [100, 101], 'qty': [1.0, 2.0]})
        >>> mirrored = create_mirrored_sides(orders)
        >>> print(mirrored)
           price  qty  side
        0    100  1.0   buy
        1    101  2.0   buy
        0    100  1.0  sell
        1    101  2.0  sell

    Notes:
        - Useful for creating symmetric order books
        - Does not modify price levels (you may want to mirror prices around mid)
        - Original index is preserved (use ignore_index=True in concat if needed)
    """
    dfs = []
    for side in sides:
        side_df = data.copy()
        side_df["side"] = side
        dfs.append(side_df)
    return pd.concat(dfs, ignore_index=True)


def is_ask_side(data: pd.DataFrame) -> pd.Series:
    """Identify ask side rows in order book.

    Handles both order book format ('asks'/'bids') and order format ('sell'/'buy').

    Args:
        data: DataFrame with 'side' column

    Returns:
        Boolean Series where True indicates ask/sell side

    Examples:
        >>> orderbook = pd.DataFrame({'side': ['bids', 'asks', 'bids']})
        >>> is_ask_side(orderbook)
        0    False
        1     True
        2    False
        dtype: bool

        >>> orders = pd.DataFrame({'side': ['buy', 'sell', 'buy']})
        >>> is_ask_side(orders)
        0    False
        1     True
        2    False
        dtype: bool

    Notes:
        - Returns True for 'asks' or 'sell'
        - Returns False for 'bids' or 'buy'
    """
    # Handle both orderbook sides (asks/bids) and order sides (sell/buy)
    return data["side"].isin(["asks", "sell"])


def side_sign(data: pd.DataFrame) -> pd.Series:
    """Get directional sign for order book sides.

    Returns +1 for asks/sell (taking liquidity), -1 for bids/buy (providing liquidity).

    Args:
        data: DataFrame with 'side' column

    Returns:
        Series with +1 for asks/sell, -1 for bids/buy

    Examples:
        >>> orderbook = pd.DataFrame({'side': ['bids', 'asks', 'bids']})
        >>> side_sign(orderbook)
        0   -1
        1    1
        2   -1
        dtype: int64

    Notes:
        - Useful for signed price calculations
        - Convention: asks = +1, bids = -1
    """
    return 2 * is_ask_side(data).astype(int) - 1


def signed_price(data: pd.DataFrame, price_col: str = "price") -> pd.Series:
    """Calculate signed price based on side.

    Multiplies price by side sign (+1 for asks, -1 for bids), useful for
    sorting order books or calculating spreads.

    Args:
        data: DataFrame with 'side' and price columns
        price_col: Name of price column (default: 'price')

    Returns:
        Series with signed prices

    Examples:
        >>> orderbook = pd.DataFrame({
        ...     'side': ['bids', 'asks'],
        ...     'price': [99.5, 100.5]
        ... })
        >>> signed_price(orderbook)
        0    -99.5
        1    100.5
        dtype: float64

    Notes:
        - Bids get negative prices
        - Asks get positive prices
        - Useful for sorting: best bid (highest) and best ask (lowest) both sort first
    """
    return side_sign(data) * data[price_col]


def sort_orderbook(
    data: pd.DataFrame,
    by_symbol: bool = True,
    by_exchange: bool = False,
    price_col: str = "price",
) -> pd.DataFrame:
    """Sort order book by symbol, side, and price levels.

    Sorts so that best bid (highest price) and best ask (lowest price) appear
    first within each symbol/exchange group.

    Args:
        data: Order book DataFrame with 'symbol', 'side', and price columns
        by_symbol: Include symbol in sort (default: True)
        by_exchange: Include exchange in sort (default: False)
        price_col: Name of price column (default: 'price')

    Returns:
        Sorted DataFrame with best prices first

    Examples:
        >>> orderbook = pd.DataFrame({
        ...     'symbol': ['BTC/USDT', 'BTC/USDT', 'BTC/USDT'],
        ...     'side': ['asks', 'bids', 'asks'],
        ...     'price': [101, 99, 100],
        ...     'qty': [1.0, 2.0, 1.5]
        ... })
        >>> sorted_ob = sort_orderbook(orderbook)
        >>> # Result: bids@99 (best bid), asks@100 (best ask), asks@101

    Notes:
        - Uses signed price for correct sorting
        - Best bid = highest bid price = most negative signed price
        - Best ask = lowest ask price = least positive signed price
        - Reset index after sort (ignore_index=True)
    """
    result = data.copy()
    result["_signed_price"] = signed_price(result, price_col)

    sort_cols = []
    if by_exchange:
        sort_cols.append("exchange")
    if by_symbol:
        sort_cols.append("symbol")
    sort_cols.extend(["side", "_signed_price"])

    result = result.sort_values(sort_cols, ignore_index=True)
    return result.drop(columns=["_signed_price"])


def calculate_notional(
    data: pd.DataFrame, price_col: str = "price", qty_col: str = "qty"
) -> pd.Series:
    """Calculate notional value (price × quantity).

    Args:
        data: DataFrame with price and quantity columns
        price_col: Name of price column (default: 'price')
        qty_col: Name of quantity column (default: 'qty')

    Returns:
        Series with notional values

    Examples:
        >>> orderbook = pd.DataFrame({'price': [100, 101], 'qty': [1.5, 2.0]})
        >>> calculate_notional(orderbook)
        0    150.0
        1    202.0
        dtype: float64

    Notes:
        - Notional = price × quantity
        - Represents total value at each price level
        - Used in VWAP and depth calculations
    """
    return data[price_col] * data[qty_col]


def calculate_vwap_by_depth(
    data: pd.DataFrame,
    depths: list | tuple | set,
    group_by: list[str] | None = None,
    price_col: str = "price",
    qty_col: str = "qty",
) -> pd.DataFrame:
    """Calculate Volume-Weighted Average Price (VWAP) at various depth levels.

    Computes the average execution price for buying/selling up to a certain
    notional depth. Useful for estimating market impact and slippage.

    Args:
        data: Order book DataFrame with price, qty, symbol, and side columns
        depths: List of notional depths to calculate VWAP for (e.g., [1000, 5000, 10000])
        group_by: Columns to group by (default: ['symbol', 'side'] + 'exchange' if present)
        price_col: Name of price column (default: 'price')
        qty_col: Name of quantity column (default: 'qty')

    Returns:
        DataFrame with columns: [*group_by, depth, qty, notional, price]
        where 'price' is the VWAP at each depth level

    Examples:
        >>> # Calculate VWAP for buying $1000 and $5000 worth
        >>> orderbook = pd.DataFrame({
        ...     'symbol': ['BTC/USDT'] * 4,
        ...     'side': ['asks'] * 4,
        ...     'price': [100, 101, 102, 103],
        ...     'qty': [10, 10, 10, 10]
        ... })
        >>> vwap = calculate_vwap_by_depth(orderbook, depths=[500, 1500])
        >>> # Shows average price to buy $500 worth (≈100) and $1500 worth (≈101)

    Notes:
        - VWAP = total notional / total quantity
        - Accounts for partial fills at the last price level
        - Order book should be pre-sorted (use sort_orderbook first)
        - Higher depths = more market impact = higher VWAP for asks, lower for bids
        - Useful for:
          - Market impact analysis
          - Slippage estimation
          - Liquidity assessment
          - Order size optimization
    """
    if group_by is None:
        group_by = ["symbol", "side"]
        if "exchange" in data.columns:
            group_by.append("exchange")

    result = data.copy()

    # Calculate notional value at each level
    result["notional"] = calculate_notional(result, price_col, qty_col)

    # Calculate cumulative notional within each group
    result["cum_notional"] = result.groupby(group_by)["notional"].cumsum()

    # Create a row for each depth level
    depth_dfs = []
    for depth in depths:
        depth_df = result.copy()
        depth_df["depth"] = depth
        depth_dfs.append(depth_df)

    # Combine all depth levels
    all_depths = pd.concat(depth_dfs, ignore_index=True)

    # Filter to rows within depth (cum_notional - notional <= depth)
    # This includes the last level that crosses the depth threshold
    within_depth = all_depths.query("(cum_notional - notional) <= depth").copy()

    group_by_with_depth = group_by + ["depth"]

    # Adjust notional for the last level (partial fill)
    # If cum_notional > depth, only use (depth - previous_cum_notional)
    within_depth["notional"] = within_depth["notional"].where(
        within_depth["cum_notional"] <= within_depth["depth"],
        other=(
            within_depth["depth"]
            - within_depth.groupby(group_by_with_depth)["cum_notional"].shift(1).fillna(0)
        ),
    )

    # Recalculate qty based on adjusted notional
    within_depth[qty_col] = within_depth["notional"] / within_depth[price_col]

    # Aggregate by group and depth
    vwap = within_depth.groupby(group_by_with_depth, as_index=False)[[qty_col, "notional"]].sum()

    # Calculate VWAP
    vwap[price_col] = vwap["notional"] / vwap[qty_col]

    return vwap


def calculate_mid_price_and_spread(
    data: pd.DataFrame,
    price_col: str = "price",
    by_exchange: bool = False,
) -> pd.DataFrame:
    """Calculate mid price, spread, and relative spread from order book for all symbols.

    Computes best bid/ask, mid price, absolute spread, and relative spread for each
    symbol (and optionally exchange) using pandas pivot for efficient calculation.

    Args:
        data: Order book DataFrame (should be sorted)
        price_col: Name of price column (default: 'price')
        by_exchange: Include exchange in grouping (default: False)

    Returns:
        DataFrame with columns: bid, ask, mid_price, spread, relative_spread
        Indexed by symbol (and optionally exchange)

    Examples:
        >>> orderbook = pd.DataFrame({
        ...     'symbol': ['BTC/USDT', 'BTC/USDT', 'ETH/USDT', 'ETH/USDT'],
        ...     'side': ['bids', 'asks', 'bids', 'asks'],
        ...     'price': [99.5, 100.5, 1800, 1820],
        ...     'qty': [10, 10, 5, 5]
        ... })
        >>> result = calculate_mid_price_and_spread(orderbook)
        >>> print(result)
                    bid     ask  mid_price  spread  relative_spread
        symbol
        BTC/USDT   99.5   100.5      100.0     1.0         0.010000
        ETH/USDT  1800.0  1820.0     1810.0    20.0         0.011050

        >>> # Access specific columns
        >>> result['mid_price']
        symbol
        BTC/USDT     100.0
        ETH/USDT    1810.0

        >>> result['spread']
        symbol
        BTC/USDT     1.0
        ETH/USDT    20.0

    Notes:
        - Order book should be sorted first (use sort_orderbook)
        - Uses pandas pivot for efficient calculation
        - mid_price = (bid + ask) / 2
        - spread = ask - bid (absolute)
        - relative_spread = spread / mid_price (as decimal, multiply by 100 for %)
        - Tighter spreads indicate higher liquidity
    """
    group_cols = (
        ["exchange", "symbol"] if by_exchange and "exchange" in data.columns else ["symbol"]
    )
    result = data.copy()
    result["side"] = result["side"].map({"asks": "ask", "bids": "bid"})
    result = result.drop_duplicates(subset=group_cols + ["side"], keep="first").pivot(
        index=group_cols, columns="side", values=price_col
    )
    result["mid_price"] = (result["bid"] + result["ask"]) / 2
    result["spread"] = result["ask"] - result["bid"]
    result["relative_spread"] = result["spread"] / result["mid_price"]
    return result[["bid", "ask", "mid_price", "spread", "relative_spread"]]
