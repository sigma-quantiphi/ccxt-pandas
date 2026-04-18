"""
Exchange-specific response parsers for implicit CCXT methods.

Each exchange has its own response envelope format. Parsers here unwrap
the envelope, look up pre-registered config for the method, and convert
to a typed DataFrame via BaseProcessor.

Adding a new exchange:
1. Define <EXCHANGE>_METHOD_CONFIG with method_name → MethodConfig mappings
2. Define <exchange>_to_dataframe(processor, result, method_name) -> pd.DataFrame
3. Register in EXCHANGE_PARSERS

Adding a new implicit method:
- Find the camelCase CCXT method name from ccxt/abstract/<exchange>.py
  (e.g. private_get_tradingbot_grid_orders_algo_pending → privateGetTradingBotGridOrdersAlgoPending)
- Add a MethodConfig entry in the appropriate exchange + category section
- data_key: key to extract from the response envelope (None = response is already the data)
- single_dict: True when the endpoint returns a single dict → one-row DataFrame
- column_names: only needed for list-of-lists; list-of-dicts uses dict keys automatically

Note: configs are keyed by camelCase. Snake_case aliases are added automatically
by _build_dual_case_config() at module load time so both forms resolve identically.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    from ccxt_pandas.wrappers.base_processor import BaseProcessor


@dataclass
class MethodConfig:
    """Parsing configuration for a single implicit exchange method.

    Attributes:
        data_key: Key to extract from the response envelope before converting
            to DataFrame (e.g. "list" for Binance earn, "data" for OKX).
            None means the response itself is the data payload.
        single_dict: When True the response is a single dict and is wrapped
            in a list to produce a one-row DataFrame.
        column_names: Column names for list-of-lists responses. Not needed
            for list-of-dicts (dict keys are used automatically).
    """

    data_key: str | None = None
    single_dict: bool = False
    column_names: tuple[str, ...] | None = None


def _build_dual_case_config(config: dict[str, MethodConfig]) -> dict[str, MethodConfig]:
    """Add snake_case aliases to a camelCase-keyed config dict.

    Uses CCXT's own un_camel_case to ensure the snake_case form matches
    exactly what __getattribute__ receives when the user calls a method
    in snake_case.
    """
    from ccxt import Exchange

    exchange = Exchange()
    aliases = {}
    for camel_name, method_config in config.items():
        snake_name = exchange.un_camel_case(camel_name)
        if snake_name != camel_name:
            aliases[snake_name] = method_config
    config.update(aliases)
    return config


# ---------------------------------------------------------------------------
# Binance (exchange_id = "binance", "binanceusdm", "binancecoinm")
# All sapi/fapi/dapi endpoints are accessible via ccxt.binance(), so configs
# are unified into a single dict.
# Abstract: https://github.com/ccxt/ccxt/blob/master/python/ccxt/abstract/binance.py
# ---------------------------------------------------------------------------

BINANCE_METHOD_CONFIG: dict[str, MethodConfig] = _build_dual_case_config(
    {
        # --- Earn: Dual Investment (sapi) ---
        # https://developers.binance.com/docs/advanced_earn/dual-investment
        # Responses enveloped: {"total": N, "list": [...]}
        # Subscribe returns a single dict.
        "sapiGetDciProductList": MethodConfig(data_key="list"),
        "sapiGetDciProductPositions": MethodConfig(data_key="list"),
        "sapiGetDciProductAccounts": MethodConfig(single_dict=True),
        "sapiPostDciProductSubscribe": MethodConfig(single_dict=True),
        "sapiPostDciProductAutoCompoundEdit": MethodConfig(single_dict=True),
        # --- Simple Earn (sapi) ---
        # https://developers.binance.com/docs/simple_earn
        # Responses enveloped: {"total": N, "rows": [...]}
        "sapiGetSimpleEarnFlexibleList": MethodConfig(data_key="rows"),
        "sapiGetSimpleEarnLockedList": MethodConfig(data_key="rows"),
        "sapiGetSimpleEarnFlexiblePosition": MethodConfig(data_key="rows"),
        "sapiGetSimpleEarnLockedPosition": MethodConfig(data_key="rows"),
        "sapiGetSimpleEarnFlexibleHistorySubscriptionRecord": MethodConfig(data_key="rows"),
        "sapiGetSimpleEarnLockedHistorySubscriptionRecord": MethodConfig(data_key="rows"),
        "sapiGetSimpleEarnFlexibleHistoryRedemptionRecord": MethodConfig(data_key="rows"),
        "sapiGetSimpleEarnLockedHistoryRedemptionRecord": MethodConfig(data_key="rows"),
        "sapiGetSimpleEarnFlexibleHistoryRewardsRecord": MethodConfig(data_key="rows"),
        "sapiGetSimpleEarnLockedHistoryRewardsRecord": MethodConfig(data_key="rows"),
        "sapiGetSimpleEarnAccount": MethodConfig(single_dict=True),
        # --- fapi data endpoints (USD-M futures) ---
        # https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data
        # Responses are direct lists (no envelope).
        # Note: camelCase matches the raw CCXT abstract exactly (mixed casing preserved).
        "fapiDataGetTakerlongshortRatio": MethodConfig(
            column_names=("timestamp", "longShortRatio", "longAccount", "shortAccount"),
        ),
        "fapiDataGetTopLongShortAccountRatio": MethodConfig(
            column_names=("timestamp", "longShortRatio", "longAccount", "shortAccount"),
        ),
        "fapiDataGetTopLongShortPositionRatio": MethodConfig(
            column_names=("timestamp", "longShortRatio", "longAccount", "shortAccount"),
        ),
        "fapiDataGetGlobalLongShortAccountRatio": MethodConfig(
            column_names=("timestamp", "longShortRatio", "longAccount", "shortAccount"),
        ),
        "fapiDataGetOpenInterestHist": MethodConfig(
            column_names=("timestamp", "sumOpenInterest", "sumOpenInterestValue"),
        ),
        # --- fapiPublic ---
        # https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data
        # Direct list responses (no envelope).
        "fapiPublicGetFundingRate": MethodConfig(),
        "fapiPublicGetPremiumIndex": MethodConfig(),
        "fapiPublicGetTicker24hr": MethodConfig(),
        "fapiPublicGetTickerPrice": MethodConfig(),
        "fapiPublicGetTickerBookTicker": MethodConfig(),
        "fapiPublicGetOpenInterest": MethodConfig(single_dict=True),
        # --- fapiPrivate ---
        # https://developers.binance.com/docs/derivatives/usds-margined-futures/account
        "fapiPrivateGetPositionRisk": MethodConfig(),
        "fapiPrivateGetAllOrders": MethodConfig(),
        "fapiPrivateGetUserTrades": MethodConfig(),
        "fapiPrivateGetIncome": MethodConfig(),
        "fapiPrivateGetBalance": MethodConfig(),
        "fapiPrivateGetAccount": MethodConfig(single_dict=True),
        "fapiPrivateGetForceOrders": MethodConfig(),
        "fapiPrivateGetAdlQuantile": MethodConfig(),
        "fapiPrivateGetCommissionRate": MethodConfig(single_dict=True),
        # --- dapi data endpoints (COIN-M futures) ---
        # https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data
        # Responses are direct lists (no envelope).
        "dapiDataGetTakerBuySellVol": MethodConfig(
            column_names=("timestamp", "buySellRatio", "buyVol", "sellVol"),
        ),
        "dapiDataGetTopLongShortAccountRatio": MethodConfig(
            column_names=("timestamp", "longShortRatio", "longAccount", "shortAccount"),
        ),
        "dapiDataGetTopLongShortPositionRatio": MethodConfig(
            column_names=("timestamp", "longShortRatio", "longAccount", "shortAccount"),
        ),
        "dapiDataGetGlobalLongShortAccountRatio": MethodConfig(
            column_names=("timestamp", "longShortRatio", "longAccount", "shortAccount"),
        ),
        "dapiDataGetOpenInterestHist": MethodConfig(
            column_names=("timestamp", "sumOpenInterest", "sumOpenInterestValue"),
        ),
        # --- dapiPublic ---
        "dapiPublicGetFundingRate": MethodConfig(),
        "dapiPublicGetPremiumIndex": MethodConfig(),
        "dapiPublicGetTicker24hr": MethodConfig(),
        "dapiPublicGetTickerPrice": MethodConfig(),
        "dapiPublicGetTickerBookTicker": MethodConfig(),
        "dapiPublicGetOpenInterest": MethodConfig(single_dict=True),
        # --- dapiPrivate ---
        "dapiPrivateGetPositionRisk": MethodConfig(),
        "dapiPrivateGetAllOrders": MethodConfig(),
        "dapiPrivateGetUserTrades": MethodConfig(),
        "dapiPrivateGetIncome": MethodConfig(),
        "dapiPrivateGetBalance": MethodConfig(),
        "dapiPrivateGetAccount": MethodConfig(single_dict=True),
        "dapiPrivateGetForceOrders": MethodConfig(),
        "dapiPrivateGetAdlQuantile": MethodConfig(),
        "dapiPrivateGetCommissionRate": MethodConfig(single_dict=True),
        # --- dapi-only data ---
        "dapiDataGetBasis": MethodConfig(),
        "dapiDataGetDeliveryPrice": MethodConfig(),
        # --- Algo: spot (sapi) ---
        # https://developers.binance.com/docs/algo/spot-algo
        # Responses enveloped: {"total": N, "orders": [...]} or {"total": N, "subOrders": [...]}
        "sapiGetAlgoSpotOpenOrders": MethodConfig(data_key="orders"),
        "sapiGetAlgoSpotHistoricalOrders": MethodConfig(data_key="orders"),
        "sapiGetAlgoSpotSubOrders": MethodConfig(data_key="subOrders"),
        "sapiPostAlgoSpotNewOrderTwap": MethodConfig(single_dict=True),
        "sapiDeleteAlgoSpotOrder": MethodConfig(single_dict=True),
        # --- Algo: futures (sapi) ---
        # https://developers.binance.com/docs/algo/future-algo
        # Responses enveloped: {"total": N, "orders": [...]} or {"total": N, "subOrders": [...]}
        "sapiGetAlgoFuturesOpenOrders": MethodConfig(data_key="orders"),
        "sapiGetAlgoFuturesHistoricalOrders": MethodConfig(data_key="orders"),
        "sapiGetAlgoFuturesSubOrders": MethodConfig(data_key="subOrders"),
        "sapiPostAlgoFuturesNewOrderTwap": MethodConfig(single_dict=True),
        "sapiPostAlgoFuturesNewOrderVp": MethodConfig(single_dict=True),
        "sapiDeleteAlgoFuturesOrder": MethodConfig(single_dict=True),
        # --- Earn: Discount Buy / Accumulator (sapi) ---
        # https://developers.binance.com/docs/advanced_earn/discount-buy
        # Product list & positions enveloped: {"total": N, "list": [...]}
        # Subscribe & sum-holding return a single dict.
        "sapiGetAccumulatorProductList": MethodConfig(data_key="list"),
        "sapiGetAccumulatorProductPositionList": MethodConfig(data_key="list"),
        "sapiGetAccumulatorProductSumHolding": MethodConfig(single_dict=True),
        "sapiPostAccumulatorProductSubscribe": MethodConfig(single_dict=True),
        # --- Algo: futures (fapi-native) ---
        # https://developers.binance.com/docs/derivatives/usds-margined-futures/trade
        "fapiPrivateGetAlgoOrder": MethodConfig(single_dict=True),
        "fapiPrivateGetOpenAlgoOrders": MethodConfig(),
        "fapiPrivateGetAllAlgoOrders": MethodConfig(),
        "fapiPrivatePostAlgoOrder": MethodConfig(single_dict=True),
        "fapiPrivateDeleteAlgoOrder": MethodConfig(single_dict=True),
        "fapiPrivateDeleteAlgoOpenOrders": MethodConfig(single_dict=True),
    }
)


def binance_to_dataframe(
    processor: BaseProcessor,
    result: list | dict,
    method_name: str,
) -> pd.DataFrame:
    """Parse a Binance implicit method response into a typed DataFrame.

    Handles sapi (spot), fapi (USD-M futures), and dapi (COIN-M futures)
    endpoints since all are accessible via ccxt.binance().

    Uses BINANCE_METHOD_CONFIG to unwrap the response envelope. Unregistered
    methods are treated as a direct list payload with no column name overrides.

    Args:
        processor: BaseProcessor instance (carries exchange-specific field sets).
        result: Raw response from the CCXT exchange method.
        method_name: camelCase CCXT method name used to look up the config.

    Returns:
        Typed DataFrame with numeric/datetime fields cast appropriately.
    """
    config = BINANCE_METHOD_CONFIG.get(method_name, MethodConfig())
    if config.single_dict:
        data = [result]
    elif config.data_key:
        data = result[config.data_key]
    else:
        data = result
    return processor.response_to_dataframe(data, column_names=config.column_names)


# ---------------------------------------------------------------------------
# OKX (exchange_id = "okx")
# Abstract: https://github.com/ccxt/ccxt/blob/master/python/ccxt/abstract/okx.py
# ---------------------------------------------------------------------------

OKX_METHOD_CONFIG: dict[str, MethodConfig] = _build_dual_case_config(
    {
        # --- Market: candlestick data ---
        # https://www.okx.com/docs-v5/en/#order-book-trading-market-data
        # Responses: {"code": "0", "data": [[ts, o, h, l, c, ...], ...], "msg": ""}
        "publicGetMarketCandles": MethodConfig(
            data_key="data",
            column_names=(
                "timestamp",
                "open",
                "high",
                "low",
                "close",
                "vol",
                "volCcy",
                "volCcyQuote",
                "confirm",
            ),
        ),
        "publicGetMarketHistoryCandles": MethodConfig(
            data_key="data",
            column_names=(
                "timestamp",
                "open",
                "high",
                "low",
                "close",
                "vol",
                "volCcy",
                "volCcyQuote",
                "confirm",
            ),
        ),
        "publicGetMarketIndexCandles": MethodConfig(
            data_key="data",
            column_names=("timestamp", "open", "high", "low", "close", "confirm"),
        ),
        "publicGetMarketMarkPriceCandles": MethodConfig(
            data_key="data",
            column_names=("timestamp", "open", "high", "low", "close", "confirm"),
        ),
        "publicGetMarketHistoryIndexCandles": MethodConfig(
            data_key="data",
            column_names=("timestamp", "open", "high", "low", "close", "confirm"),
        ),
        "publicGetMarketHistoryMarkPriceCandles": MethodConfig(
            data_key="data",
            column_names=("timestamp", "open", "high", "low", "close", "confirm"),
        ),
        # --- Rubik Statistics ---
        # https://www.okx.com/docs-v5/en/#trading-statistics-rest-api
        # Responses: {"code": "0", "data": [[...], ...], "msg": ""}
        "publicGetRubikStatContractsLongShortAccountRatio": MethodConfig(
            data_key="data",
            column_names=("timestamp", "longShortRatio"),
        ),
        "publicGetRubikStatContractsLongShortAccountRatioContract": MethodConfig(
            data_key="data",
            column_names=("timestamp", "longShortRatio"),
        ),
        "publicGetRubikStatContractsLongShortAccountRatioContractTopTrader": MethodConfig(
            data_key="data",
            column_names=("timestamp", "longShortRatio"),
        ),
        "publicGetRubikStatContractsOpenInterestHistory": MethodConfig(
            data_key="data",
            column_names=("timestamp", "oi", "oiCcy", "oiUsd"),
        ),
        "publicGetRubikStatContractsOpenInterestVolume": MethodConfig(
            data_key="data",
            column_names=("timestamp", "oi", "vol"),
        ),
        "publicGetRubikStatMarginLoanRatio": MethodConfig(
            data_key="data",
            column_names=("timestamp", "ratio"),
        ),
        "publicGetRubikStatTakerVolume": MethodConfig(
            data_key="data",
            column_names=("timestamp", "sellVol", "buyVol"),
        ),
        "publicGetRubikStatTakerVolumeContract": MethodConfig(
            data_key="data",
            column_names=("timestamp", "sellVol", "buyVol"),
        ),
        "publicGetRubikStatOptionOpenInterestVolume": MethodConfig(
            data_key="data",
            column_names=("timestamp", "callOI", "putOI", "callVol", "putVol"),
        ),
        "publicGetRubikStatOptionOpenInterestVolumeRatio": MethodConfig(
            data_key="data",
            column_names=("timestamp", "oiRatio", "volRatio"),
        ),
        "publicGetRubikStatOptionOpenInterestVolumeExpiry": MethodConfig(
            data_key="data",
            column_names=("timestamp", "expTime", "callOI", "putOI", "callVol", "putVol"),
        ),
        "publicGetRubikStatOptionOpenInterestVolumeStrike": MethodConfig(
            data_key="data",
            column_names=("timestamp", "strike", "callOI", "putOI", "callVol", "putVol"),
        ),
        "publicGetRubikStatOptionTakerBlockVolume": MethodConfig(
            data_key="data",
            column_names=("timestamp", "blockBuyVol", "blockSellVol"),
        ),
        # --- Market data (list-of-dicts) ---
        # https://www.okx.com/docs-v5/en/#order-book-trading-market-data
        "publicGetMarketTickers": MethodConfig(data_key="data"),
        "publicGetMarketTicker": MethodConfig(data_key="data"),
        "publicGetMarketTrades": MethodConfig(data_key="data"),
        "publicGetMarketHistoryTrades": MethodConfig(data_key="data"),
        "publicGetMarketIndexTickers": MethodConfig(data_key="data"),
        "publicGetMarketBlockTickers": MethodConfig(data_key="data"),
        "publicGetMarketBlockTicker": MethodConfig(data_key="data"),
        "publicGetMarketPlatform24Volume": MethodConfig(data_key="data"),
        "publicGetMarketExchangeRate": MethodConfig(data_key="data"),
        # --- Public instruments / funding ---
        # https://www.okx.com/docs-v5/en/#public-data-rest-api
        "publicGetPublicInstruments": MethodConfig(data_key="data"),
        "publicGetPublicFundingRate": MethodConfig(data_key="data"),
        "publicGetPublicFundingRateHistory": MethodConfig(data_key="data"),
        "publicGetPublicOpenInterest": MethodConfig(data_key="data"),
        "publicGetPublicMarkPrice": MethodConfig(data_key="data"),
        "publicGetPublicPriceLimit": MethodConfig(data_key="data"),
        "publicGetPublicOptSummary": MethodConfig(data_key="data"),
        "publicGetPublicInsuranceFund": MethodConfig(data_key="data"),
        "publicGetPublicPositionTiers": MethodConfig(data_key="data"),
        "publicGetPublicPremiumHistory": MethodConfig(data_key="data"),
        "publicGetPublicSettlementHistory": MethodConfig(data_key="data"),
        "publicGetPublicDeliveryExerciseHistory": MethodConfig(data_key="data"),
        "publicGetPublicEstimatedPrice": MethodConfig(data_key="data"),
        # --- Private account / trade ---
        # https://www.okx.com/docs-v5/en/#trading-account-rest-api
        "privateGetAccountBalance": MethodConfig(data_key="data"),
        "privateGetAccountPositions": MethodConfig(data_key="data"),
        "privateGetAccountPositionsHistory": MethodConfig(data_key="data"),
        "privateGetAccountBills": MethodConfig(data_key="data"),
        "privateGetAccountBillsArchive": MethodConfig(data_key="data"),
        "privateGetAccountGreeks": MethodConfig(data_key="data"),
        "privateGetAccountConfig": MethodConfig(data_key="data"),
        "privateGetAccountInterestAccrued": MethodConfig(data_key="data"),
        "privateGetAccountLeverageInfo": MethodConfig(data_key="data"),
        "privateGetTradeFills": MethodConfig(data_key="data"),
        "privateGetTradeFillsHistory": MethodConfig(data_key="data"),
        "privateGetTradeOrdersPending": MethodConfig(data_key="data"),
        "privateGetTradeOrdersHistory": MethodConfig(data_key="data"),
        "privateGetTradeOrdersHistoryArchive": MethodConfig(data_key="data"),
        "privateGetTradeOrdersAlgoPending": MethodConfig(data_key="data"),
        "privateGetTradeOrdersAlgoHistory": MethodConfig(data_key="data"),
        # --- Private finance: general staking ---
        # https://www.okx.com/docs-v5/en/#financial-product-rest-api
        "privateGetFinanceStakingDefiOffers": MethodConfig(data_key="data"),
        "privateGetFinanceStakingDefiOrdersActive": MethodConfig(data_key="data"),
        "privateGetFinanceStakingDefiOrdersHistory": MethodConfig(data_key="data"),
        # --- Simple Earn (savings) ---
        # https://www.okx.com/docs-v5/en/#financial-product-earn-simple-earn-flexible
        "privateGetFinanceSavingsBalance": MethodConfig(data_key="data"),
        "privateGetFinanceSavingsLendingHistory": MethodConfig(data_key="data"),
        "privatePostFinanceSavingsPurchaseRedempt": MethodConfig(data_key="data", single_dict=True),
        "privatePostFinanceSavingsSetLendingRate": MethodConfig(data_key="data", single_dict=True),
        "publicGetFinanceSavingsLendingRateSummary": MethodConfig(data_key="data"),
        "publicGetFinanceSavingsLendingRateHistory": MethodConfig(data_key="data"),
        # --- ETH Staking ---
        # https://www.okx.com/docs-v5/en/#financial-product-earn-eth-staking
        "privateGetFinanceStakingDefiEthProductInfo": MethodConfig(data_key="data"),
        "privateGetFinanceStakingDefiEthBalance": MethodConfig(data_key="data"),
        "privateGetFinanceStakingDefiEthPurchaseRedeemHistory": MethodConfig(data_key="data"),
        "privatePostFinanceStakingDefiEthPurchase": MethodConfig(data_key="data", single_dict=True),
        "privatePostFinanceStakingDefiEthRedeem": MethodConfig(data_key="data", single_dict=True),
        "privatePostFinanceStakingDefiEthCancelRedeem": MethodConfig(
            data_key="data", single_dict=True
        ),
        "publicGetFinanceStakingDefiEthApyHistory": MethodConfig(data_key="data"),
        # --- SOL Staking ---
        # https://www.okx.com/docs-v5/en/#financial-product-earn-sol-staking
        "privateGetFinanceStakingDefiSolProductInfo": MethodConfig(data_key="data"),
        "privateGetFinanceStakingDefiSolBalance": MethodConfig(data_key="data"),
        "privateGetFinanceStakingDefiSolPurchaseRedeemHistory": MethodConfig(data_key="data"),
        "privatePostFinanceStakingDefiSolPurchase": MethodConfig(data_key="data", single_dict=True),
        "privatePostFinanceStakingDefiSolRedeem": MethodConfig(data_key="data", single_dict=True),
        "privatePostFinanceStakingDefiSolCancelRedeem": MethodConfig(
            data_key="data", single_dict=True
        ),
        "publicGetFinanceStakingDefiSolApyHistory": MethodConfig(data_key="data"),
        # --- Flexible Loan ---
        # https://www.okx.com/docs-v5/en/#financial-product-earn-flexible-loan
        "privateGetFinanceFlexibleLoanBorrowCurrencies": MethodConfig(data_key="data"),
        "privateGetFinanceFlexibleLoanCollateralAssets": MethodConfig(data_key="data"),
        "privateGetFinanceFlexibleLoanLoanInfo": MethodConfig(data_key="data"),
        "privateGetFinanceFlexibleLoanLoanHistory": MethodConfig(data_key="data"),
        "privateGetFinanceFlexibleLoanInterestAccrued": MethodConfig(data_key="data"),
        "privateGetFinanceFlexibleLoanMaxCollateralRedeemAmount": MethodConfig(
            data_key="data", single_dict=True
        ),
        "privatePostFinanceFlexibleLoanMaxLoan": MethodConfig(data_key="data", single_dict=True),
        "privatePostFinanceFlexibleLoanAdjustCollateral": MethodConfig(
            data_key="data", single_dict=True
        ),
        # --- Spread trading ---
        # https://www.okx.com/docs-v5/en/#spread-trading-rest-api
        # Public endpoints
        "publicGetSprdSpreads": MethodConfig(data_key="data"),
        "publicGetSprdTicker": MethodConfig(data_key="data"),
        "publicGetSprdPublicTrades": MethodConfig(data_key="data"),
        "publicGetMarketSprdCandles": MethodConfig(
            data_key="data",
            column_names=("timestamp", "open", "high", "low", "close", "vol", "confirm"),
        ),
        "publicGetMarketSprdHistoryCandles": MethodConfig(
            data_key="data",
            column_names=("timestamp", "open", "high", "low", "close", "vol", "confirm"),
        ),
        # Private endpoints (GET)
        "privateGetSprdOrder": MethodConfig(data_key="data"),
        "privateGetSprdOrdersPending": MethodConfig(data_key="data"),
        "privateGetSprdOrdersHistory": MethodConfig(data_key="data"),
        "privateGetSprdOrdersHistoryArchive": MethodConfig(data_key="data"),
        "privateGetSprdTrades": MethodConfig(data_key="data"),
        # Private endpoints (POST) — order management, return single-dict confirmations
        "privatePostSprdOrder": MethodConfig(data_key="data", single_dict=True),
        "privatePostSprdCancelOrder": MethodConfig(data_key="data", single_dict=True),
        "privatePostSprdMassCancel": MethodConfig(data_key="data", single_dict=True),
        "privatePostSprdAmendOrder": MethodConfig(data_key="data", single_dict=True),
        "privatePostSprdCancelAllAfter": MethodConfig(data_key="data", single_dict=True),
        # --- Grid trading (trading bot) ---
        # https://www.okx.com/docs-v5/en/#order-book-trading-grid-trading
        # Responses: {"code": "0", "data": [{...}, ...], "msg": ""}
        "privateGetTradingBotGridOrdersAlgoPending": MethodConfig(data_key="data"),
        "privateGetTradingBotGridOrdersAlgoHistory": MethodConfig(data_key="data"),
        "privateGetTradingBotGridOrdersAlgoDetails": MethodConfig(data_key="data"),
        "privateGetTradingBotGridSubOrders": MethodConfig(data_key="data"),
        "privateGetTradingBotGridPositions": MethodConfig(data_key="data"),
        # --- Signal trading (trading bot) ---
        "privateGetTradingBotSignalOrdersAlgoPending": MethodConfig(data_key="data"),
        "privateGetTradingBotSignalOrdersAlgoHistory": MethodConfig(data_key="data"),
        "privateGetTradingBotSignalOrdersAlgoDetails": MethodConfig(data_key="data"),
        "privateGetTradingBotSignalPositions": MethodConfig(data_key="data"),
        "privateGetTradingBotSignalPositionsHistory": MethodConfig(data_key="data"),
        "privateGetTradingBotSignalSubOrders": MethodConfig(data_key="data"),
        # --- Recurring buy (trading bot) ---
        "privateGetTradingBotRecurringOrdersAlgoPending": MethodConfig(data_key="data"),
        "privateGetTradingBotRecurringOrdersAlgoHistory": MethodConfig(data_key="data"),
        "privateGetTradingBotRecurringOrdersAlgoDetails": MethodConfig(data_key="data"),
        "privateGetTradingBotRecurringSubOrders": MethodConfig(data_key="data"),
    }
)


def okx_to_dataframe(
    processor: BaseProcessor,
    result: dict,
    method_name: str,
) -> pd.DataFrame:
    """Parse an OKX implicit method response into a typed DataFrame.

    OKX implicit methods return a standard envelope:
        {"code": "0", "data": [...], "msg": ""}
    Uses OKX_METHOD_CONFIG to determine the data_key and optional column names.
    Unregistered methods default to extracting response["data"] with no column
    name overrides.

    Args:
        processor: BaseProcessor instance (carries exchange-specific field sets).
        result: Raw response dict from the CCXT exchange method.
        method_name: camelCase CCXT method name used to look up the config.

    Returns:
        Typed DataFrame with numeric/datetime fields cast appropriately.
    """
    config = OKX_METHOD_CONFIG.get(method_name, MethodConfig(data_key="data"))
    if config.single_dict:
        data = [result]
    elif config.data_key:
        data = result[config.data_key]
    else:
        data = result
    return processor.response_to_dataframe(data, column_names=config.column_names)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

EXCHANGE_PARSERS: dict[str, Callable] = {
    "binance": binance_to_dataframe,
    "binanceusdm": binance_to_dataframe,
    "binancecoinm": binance_to_dataframe,
    "okx": okx_to_dataframe,
}


def get_parser(exchange_name: str | None) -> Callable | None:
    """Return the response parser for a known exchange, or None if unregistered.

    When None is returned the caller should pass the raw result through unchanged.
    """
    return EXCHANGE_PARSERS.get(exchange_name)
