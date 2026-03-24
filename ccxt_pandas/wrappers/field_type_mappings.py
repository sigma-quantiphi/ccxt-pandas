"""
Field type mappings for exchange-specific DataFrame parsing.

Organizes numeric, bool, and datetime field sets by exchange so that
BaseProcessor can apply the right type casts for both standard CCXT methods
and implicit/undocumented exchange methods.

Structure:
- CCXT_*      — standard fields present in CCXT unified API responses
- BINANCE_*   — Binance-specific fields (implicit methods, futures data, etc.)
- OKX_*       — OKX-specific fields (grid trading, implicit methods, etc.)
- DEFAULT_*   — union of all known fields; used for unrecognised exchanges
"""

# ---------------------------------------------------------------------------
# CCXT standard fields (exchange-agnostic)
# ---------------------------------------------------------------------------

CCXT_NUMERIC_FIELDS: frozenset[str] = frozenset(
    {
        "amountBorrowed",
        "ask",
        "askImpliedVolatility",
        "askPrice",
        "askSize",
        "askVolume",
        "availableBalance",
        "average",
        "baseRate",
        "baseVolume",
        "bid",
        "bidImpliedVolatility",
        "bidPrice",
        "bidSize",
        "bidVolume",
        "change",
        "close",
        "collateral",
        "collateralMarginLevel",
        "contractSize",
        "contracts",
        "cost",
        "crossUnPnl",
        "crossWalletBalance",
        "delta",
        "entryPrice",
        "estimatedSettlePrice",
        "exercisePrice",
        "fee",
        "fee_cost",
        "fee_rate",
        "free",
        "freeze",
        "fundingRate",
        "gamma",
        "high",
        "indexPrice",
        "initialMargin",
        "initialMarginPercentage",
        "interest",
        "interestRate",
        "last",
        "lastPrice",
        "leverage",
        "liquidationPrice",
        "locked",
        "low",
        "maker",
        "maintMargin",
        "maintenanceMargin",
        "maintenanceMarginPercentage",
        "marginBalance",
        "marginLevel",
        "marginRatio",
        "markImpliedVolatility",
        "markPrice",
        "maxNotional",
        "maxWithdrawAmount",
        "network_fee",
        "network_precision",
        "network_limits_withdraw_min",
        "network_limits_withdraw_max",
        "network_limits_deposit_min",
        "nextFundingRate",
        "nonce",
        "notional",
        "open",
        "openOrderInitialMargin",
        "period",
        "positionAmount",
        "positionInitialMargin",
        "precision",
        "previousClose",
        "previousFundingRate",
        "price",
        "quantity",
        "quoteRate",
        "quoteVolume",
        "realStrikePrice",
        "rho",
        "strike",
        "strikePrice",
        "taker",
        "theta",
        "totalAssetOfBtc",
        "totalCollateralValueInUSDT",
        "totalLiabilityOfBtc",
        "totalNetAssetOfBtc",
        "underlyingPrice",
        "unrealizedPnl",
        "unrealizedProfit",
        "vega",
        "vwap",
        "walletBalance",
        "withdrawing",
    }
)

CCXT_BOOL_FIELDS: frozenset[str] = frozenset(
    {
        "active",
        "contract",
        "deposit",
        "inverse",
        "linear",
        "withdraw",
        "network_active",
        "network_deposit",
        "network_withdraw",
    }
)

CCXT_INT_TO_DATETIME_FIELDS: frozenset[str] = frozenset(
    {
        "createTime",
        "created",
        "createDate",
        "expiry",
        "expiryDate",
        "fundingTimestamp",
        "lastTradeTimestamp",
        "lastUpdateTimestamp",
        "nextFundingTimestamp",
        "previousFundingTimestamp",
        "time",
        "timestamp",
        "updateTime",
    }
)

CCXT_STR_TO_DATETIME_FIELDS: frozenset[str] = frozenset(
    {
        "datetime",
        "expiryDatetime",
        "fundingDatetime",
        "nextFundingDatetime",
        "previousFundingDatetime",
    }
)

# ---------------------------------------------------------------------------
# Binance (exchange_id = "binance", "binanceusdm", "binancecoinm")
# All sapi/fapi/dapi endpoints are accessible via ccxt.binance(), so field
# sets are unified.
# Sources:
#   https://developers.binance.com/docs/advanced_earn/dual-investment
#   https://developers.binance.com/docs/simple_earn
#   https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data
#   https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data
# ---------------------------------------------------------------------------

BINANCE_NUMERIC_FIELDS: frozenset[str] = frozenset(
    {
        # sapi — earn / DCI
        "CMCCirculatingSupply",
        "apr",
        "maxAmount",
        "minAmount",
        "subscriptionAmount",
        # sapi — Simple Earn
        "latestAnnualPercentageRate",
        "tierAnnualPercentageRate",
        "totalAmount",
        "purchasedAmount",
        "redeemingAmount",
        "freeAmount",
        "freezeAmount",
        "amount",
        "cumRewardAmount",
        "realTimeRewards",
        "totalInvestedInUSD",
        "roi",
        "pnlInUSD",
        # fapi/dapi — data endpoints
        "buySellRatio",
        "buyVol",
        "longAccount",
        "longLeverage",
        "longPosition",
        "longShortRatio",
        "sellVol",
        "shortAccount",
        "shortLeverage",
        "shortPosition",
        "sumOpenInterest",
        "sumOpenInterestValue",
        # fapi/dapi — position/account
        "unRealizedProfit",
        "positionAmt",
        "isolatedMargin",
        "isolatedWallet",
        "maxNotionalValue",
        # fapi/dapi — trades
        "qty",
        "quoteQty",
        "commission",
        # fapi/dapi — funding/premium
        "lastFundingRate",
        "estimatedSettlePrice",
        # fapi/dapi — ticker
        "priceChange",
        "priceChangePercent",
        "weightedAvgPrice",
        "lastQty",
        "openPrice",
        "highPrice",
        "lowPrice",
        # fapi/dapi — commission
        "makerCommissionRate",
        "takerCommissionRate",
        # Algo trading
        "totalQty",
        "executedQty",
        "executedAmt",
        "avgPrice",
        "feeAmt",
        "origQty",
    }
)

BINANCE_BOOL_FIELDS: frozenset[str] = frozenset()

BINANCE_INT_TO_DATETIME_FIELDS: frozenset[str] = frozenset(
    {
        "createTimestamp",
        "purchaseEndTime",
        "purchaseTime",
        "settleDate",
        "fundingTime",
        "nextFundingTime",
        "openTime",
        "closeTime",
        "bookTime",
        "endTime",
    }
)

BINANCE_STR_TO_DATETIME_FIELDS: frozenset[str] = frozenset()

# ---------------------------------------------------------------------------
# OKX-specific fields
# Sources:
#   https://www.okx.com/docs-v5/en/#order-book-trading-grid-trading-get-grid-algo-order-list
#   https://www.okx.com/docs-v5/en/#order-book-trading-grid-trading-get-grid-algo-order-positions
# ---------------------------------------------------------------------------

OKX_NUMERIC_FIELDS: frozenset[str] = frozenset(
    {
        "actualLever",
        "adl",
        "annualizedRate",
        "arbitrageNum",
        "availEq",
        "avgPx",
        "baseSz",
        "curBaseSz",
        "curQuoteSz",
        "fee",
        "floatProfit",
        "fundingFee",
        "gridNum",
        "gridProfit",
        "imr",
        "investment",
        "lever",
        "liqPx",
        "markPx",
        "maxPx",
        "maxSz",
        "mgnRatio",
        "minPx",
        "minSz",
        "notionalUsd",
        "ordFrozen",
        "pnl",
        "pnlRatio",
        "pos",
        "profit",
        "profitSharingRatio",
        "px",
        "quoteSz",
        "realizedPnl",
        "rebateTrans",
        "runPx",
        "slTriggerPx",
        "stepSz",
        "sz",
        "totalAnnualizedRate",
        "totalPnl",
        "tpTriggerPx",
        "upl",
        "uplRatio",
        # Rubik stats
        "oi",
        "oiCcy",
        "oiUsd",
        "ratio",
        "callOI",
        "putOI",
        "callVol",
        "putVol",
        "oiRatio",
        "volRatio",
        "blockBuyVol",
        "blockSellVol",
        # Market data
        "askPx",
        "askSz",
        "bidPx",
        "bidSz",
        "lastSz",
        "open24h",
        "high24h",
        "low24h",
        "vol24h",
        "volCcy24h",
        "sodUtc0",
        "sodUtc8",
        # Account/trade/finance
        "availBal",
        "cashBal",
        "eq",
        "eqUsd",
        "frozenBal",
        "totalEq",
        "isoEq",
        "mmr",
        "notionalCcy",
        "accFillSz",
        "fillPx",
        "fillSz",
        "margin",
        "openAvgPx",
        "closeAvgPx",
        "apy",
        "rate",
        "amt",
        "earnings",
        # ETH/SOL staking
        "stakingAmt",
        "redeemAmt",
        "investAmt",
        "earningAmt",
        "latestApy",
        "curApy",
        "rewardAmt",
        "purchaseAmt",
        "pendingAmt",
        "canRedeemAmt",
        "redeemingAmt",
        # Simple Earn (savings)
        "lendingAmt",
        "pendingEarnings",
        "lendingRate",
        "avgRate",
        "preRate",
        "estRate",
        # Flexible Loan
        "maxLoan",
        "borrowAmt",
        "curRate",
        "collateralAmt",
        "maxCollateral",
        "minCollateral",
        "availCollateralAmt",
        "usedCollateralAmt",
        "interestAmt",
        "accruedInterest",
        "liqdPx",
        "ltv",
        "initialLtv",
        "maxLtv",
        "liqLtv",
        "availLoan",
        "maxRedeemAmt",
        # Spread trading
        "sprdPx",
        "legs_px",
        "legs_sz",
        "legs_szCont",
        "spreadId",
    }
)

OKX_BOOL_FIELDS: frozenset[str] = frozenset()

OKX_INT_TO_DATETIME_FIELDS: frozenset[str] = frozenset(
    {"cTime", "uTime", "ts", "fillTime", "expTime"}
)

OKX_STR_TO_DATETIME_FIELDS: frozenset[str] = frozenset()

# ---------------------------------------------------------------------------
# Registry: exchange_id → exchange-specific sets
# ---------------------------------------------------------------------------

EXCHANGE_NUMERIC_FIELDS: dict[str, frozenset[str]] = {
    "binance": BINANCE_NUMERIC_FIELDS,
    "binanceusdm": BINANCE_NUMERIC_FIELDS,
    "binancecoinm": BINANCE_NUMERIC_FIELDS,
    "okx": OKX_NUMERIC_FIELDS,
}

EXCHANGE_BOOL_FIELDS: dict[str, frozenset[str]] = {
    "binance": BINANCE_BOOL_FIELDS,
    "binanceusdm": BINANCE_BOOL_FIELDS,
    "binancecoinm": BINANCE_BOOL_FIELDS,
    "okx": OKX_BOOL_FIELDS,
}

EXCHANGE_INT_TO_DATETIME_FIELDS: dict[str, frozenset[str]] = {
    "binance": BINANCE_INT_TO_DATETIME_FIELDS,
    "binanceusdm": BINANCE_INT_TO_DATETIME_FIELDS,
    "binancecoinm": BINANCE_INT_TO_DATETIME_FIELDS,
    "okx": OKX_INT_TO_DATETIME_FIELDS,
}

EXCHANGE_STR_TO_DATETIME_FIELDS: dict[str, frozenset[str]] = {
    "binance": BINANCE_STR_TO_DATETIME_FIELDS,
    "binanceusdm": BINANCE_STR_TO_DATETIME_FIELDS,
    "binancecoinm": BINANCE_STR_TO_DATETIME_FIELDS,
    "okx": OKX_STR_TO_DATETIME_FIELDS,
}

# ---------------------------------------------------------------------------
# Defaults: union of all known exchange fields (fallback for unknown exchanges)
# ---------------------------------------------------------------------------

DEFAULT_NUMERIC_FIELDS: frozenset[str] = (
    CCXT_NUMERIC_FIELDS
    | BINANCE_NUMERIC_FIELDS
    | OKX_NUMERIC_FIELDS
)

DEFAULT_BOOL_FIELDS: frozenset[str] = (
    CCXT_BOOL_FIELDS
    | BINANCE_BOOL_FIELDS
    | OKX_BOOL_FIELDS
)

DEFAULT_INT_TO_DATETIME_FIELDS: frozenset[str] = (
    CCXT_INT_TO_DATETIME_FIELDS
    | BINANCE_INT_TO_DATETIME_FIELDS
    | OKX_INT_TO_DATETIME_FIELDS
)

DEFAULT_STR_TO_DATETIME_FIELDS: frozenset[str] = (
    CCXT_STR_TO_DATETIME_FIELDS
    | BINANCE_STR_TO_DATETIME_FIELDS
    | OKX_STR_TO_DATETIME_FIELDS
)

# ---------------------------------------------------------------------------
# Getter functions
# ---------------------------------------------------------------------------


def get_numeric_fields(exchange_name: str | None) -> frozenset[str]:
    """Return the numeric field set for an exchange.

    Known exchange → CCXT_NUMERIC_FIELDS | <exchange>_NUMERIC_FIELDS.
    Unknown exchange → DEFAULT_NUMERIC_FIELDS (union of all registered sets).
    """
    if exchange_name in EXCHANGE_NUMERIC_FIELDS:
        return CCXT_NUMERIC_FIELDS | EXCHANGE_NUMERIC_FIELDS[exchange_name]
    return DEFAULT_NUMERIC_FIELDS


def get_bool_fields(exchange_name: str | None) -> frozenset[str]:
    """Return the boolean field set for an exchange.

    Known exchange → CCXT_BOOL_FIELDS | <exchange>_BOOL_FIELDS.
    Unknown exchange → DEFAULT_BOOL_FIELDS.
    """
    if exchange_name in EXCHANGE_BOOL_FIELDS:
        return CCXT_BOOL_FIELDS | EXCHANGE_BOOL_FIELDS[exchange_name]
    return DEFAULT_BOOL_FIELDS


def get_int_to_datetime_fields(exchange_name: str | None) -> frozenset[str]:
    """Return the integer-timestamp-to-datetime field set for an exchange.

    Known exchange → CCXT_INT_TO_DATETIME_FIELDS | <exchange>_INT_TO_DATETIME_FIELDS.
    Unknown exchange → DEFAULT_INT_TO_DATETIME_FIELDS.
    """
    if exchange_name in EXCHANGE_INT_TO_DATETIME_FIELDS:
        return CCXT_INT_TO_DATETIME_FIELDS | EXCHANGE_INT_TO_DATETIME_FIELDS[exchange_name]
    return DEFAULT_INT_TO_DATETIME_FIELDS


def get_str_to_datetime_fields(exchange_name: str | None) -> frozenset[str]:
    """Return the string-timestamp-to-datetime field set for an exchange.

    Known exchange → CCXT_STR_TO_DATETIME_FIELDS | <exchange>_STR_TO_DATETIME_FIELDS.
    Unknown exchange → DEFAULT_STR_TO_DATETIME_FIELDS.
    """
    if exchange_name in EXCHANGE_STR_TO_DATETIME_FIELDS:
        return CCXT_STR_TO_DATETIME_FIELDS | EXCHANGE_STR_TO_DATETIME_FIELDS[exchange_name]
    return DEFAULT_STR_TO_DATETIME_FIELDS
