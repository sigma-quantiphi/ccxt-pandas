"""Market, ticker, and funding rate data schema."""

from typing import Optional

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class MarketSchema(BaseExchangeSchema):
    """Market/ticker/funding rate data schema.

    Used by methods like load_markets, fetch_tickers, fetch_funding_rates,
    fetch_market_leverage_tiers, etc.

    Based on analysis of 20 exchanges, only 13 fields are ALWAYS present.
    All other fields are Optional even if very common.
    """

    # Core identifiers
    id: Series[str] = pa.Field(
        unique=True, title="Market ID", description="Exchange-specific market ID"
    )
    symbol: Series[str] = pa.Field(
        unique=True, title="Symbol", description="Unified CCXT market symbol"
    )
    base: Series[str] = pa.Field(title="Base Currency", description="Base currency")
    quote: Series[str] = pa.Field(title="Quote Currency", description="Quote currency")
    baseId: Series[str] = pa.Field(
        title="Base ID", description="Exchange-specific base currency ID"
    )
    quoteId: Series[str] = pa.Field(
        title="Quote ID", description="Exchange-specific quote currency ID"
    )

    # Market type
    type: Series[str] = pa.Field(
        isin=["spot", "swap", "future", "option"],
        title="Market Type",
        description="Market type",
    )

    # Market type booleans (always present)
    spot: Series[bool] = pa.Field(title="Spot", description="Is spot market")
    swap: Series[bool] = pa.Field(title="Swap", description="Is perpetual swap")
    future: Series[bool] = pa.Field(title="Future", description="Is futures contract")
    option: Series[bool] = pa.Field(title="Option", description="Is options contract")
    contract: Series[bool] = pa.Field(
        title="Contract", description="Is a contract market"
    )

    # ========================================================================
    # OPTIONAL FIELDS
    # ========================================================================

    # Additional identifiers
    lowercaseId: Optional[Series[str]] = pa.Field(
        nullable=True,
        title="Lowercase ID",
        description="Lowercase version of exchange ID",
    )
    settle: Optional[Series[str]] = pa.Field(
        nullable=True,
        title="Settlement Currency",
        description="Settlement currency (for futures/swaps)",
    )
    settleId: Optional[Series[str]] = pa.Field(
        nullable=True,
        title="Settlement ID",
        description="Exchange-specific settlement currency ID",
    )

    # Market status (missing in bit2c)
    active: Optional[Series[bool]] = pa.Field(
        nullable=True,
        title="Active",
        description="Whether market is active for trading",
    )

    # Margin (missing in some, AND can be object type in ascendex, not bool!)
    margin: Optional[Series[bool]] = pa.Field(
        nullable=True, title="Margin", description="Supports margin trading"
    )

    # Contract details (14/19 each)
    linear: Optional[Series[bool]] = pa.Field(
        nullable=True, title="Linear", description="Linear contract (settled in quote)"
    )
    inverse: Optional[Series[bool]] = pa.Field(
        nullable=True, title="Inverse", description="Inverse contract (settled in base)"
    )
    subType: Optional[Series[str]] = pa.Field(
        nullable=True, title="Subtype", description="Market subtype"
    )
    contractSize: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Contract Size", description="Size of one contract"
    )

    # Expiry and options (only in 5/19 exchanges)
    expiry: Optional[Series[pd.Timestamp]] = pa.Field(
        nullable=True, title="Expiry", description="Expiry timestamp (as datetime)"
    )
    expiryDatetime: Optional[Series[pd.Timestamp]] = pa.Field(
        nullable=True, title="Expiry Datetime", description="Expiry datetime (alias)"
    )
    strike: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Strike Price", description="Strike price (options)"
    )
    optionType: Optional[Series[str]] = pa.Field(
        nullable=True,
        isin=["call", "put"],
        title="Option Type",
        description="Option type",
    )

    # Creation timestamp (7/19)
    created: Optional[Series[pd.Timestamp]] = pa.Field(
        nullable=True, title="Created", description="Market creation timestamp"
    )

    # Fee structure (15-16/19)
    taker: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Taker Fee", description="Taker fee rate"
    )
    maker: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, title="Maker Fee", description="Maker fee rate"
    )
    tierBased: Optional[Series[bool]] = pa.Field(
        nullable=True, title="Tier Based", description="Whether fees are tier-based"
    )
    percentage: Optional[Series[bool]] = pa.Field(
        nullable=True,
        title="Percentage",
        description="Whether fees are percentage-based",
    )
    feeSide: Optional[Series[str]] = pa.Field(
        nullable=True,
        isin=["get", "give", "base", "quote", "other"],
        title="Fee Side",
        description="Which side pays the fee",
    )

    # Precision (17/19 for amount/price, but can be int64 in some exchanges!)
    precision_amount: Optional[Series[float]] = pa.Field(
        nullable=True,
        title="Amount Precision",
        description="Amount precision (decimal places or tick size)",
    )
    precision_price: Optional[Series[float]] = pa.Field(
        nullable=True,
        title="Price Precision",
        description="Price precision (decimal places or tick size)",
    )
    precision_base: Optional[Series[float]] = pa.Field(
        nullable=True, title="Base Precision", description="Base currency precision"
    )
    precision_quote: Optional[Series[float]] = pa.Field(
        nullable=True, title="Quote Precision", description="Quote currency precision"
    )

    # Limits - Amount (16/19 for min, 13/19 for max)
    # Note: Column names use dot notation (limits_amount.min)
    limits_amount_min: Optional[Series[float]] = pa.Field(
        ge=0,
        nullable=True,
        alias="limits_amount.min",
        title="Min Amount",
        description="Minimum order amount",
    )
    limits_amount_max: Optional[Series[float]] = pa.Field(
        ge=0,
        nullable=True,
        alias="limits_amount.max",
        title="Max Amount",
        description="Maximum order amount",
    )

    # Limits - Price (14/19 for min, 10/19 for max)
    limits_price_min: Optional[Series[float]] = pa.Field(
        ge=0,
        nullable=True,
        alias="limits_price.min",
        title="Min Price",
        description="Minimum order price",
    )
    limits_price_max: Optional[Series[float]] = pa.Field(
        ge=0,
        nullable=True,
        alias="limits_price.max",
        title="Max Price",
        description="Maximum order price",
    )

    # Limits - Cost (12/19 for min, 5/19 for max)
    limits_cost_min: Optional[Series[float]] = pa.Field(
        ge=0,
        nullable=True,
        alias="limits_cost.min",
        title="Min Cost",
        description="Minimum order cost",
    )
    limits_cost_max: Optional[Series[float]] = pa.Field(
        ge=0,
        nullable=True,
        alias="limits_cost.max",
        title="Max Cost",
        description="Maximum order cost",
    )

    # Limits - Market (only 5/19 - Binance variants and Aster)
    limits_market_min: Optional[Series[float]] = pa.Field(
        ge=0,
        nullable=True,
        alias="limits_market.min",
        title="Min Market Size",
        description="Minimum market order size",
    )
    limits_market_max: Optional[Series[float]] = pa.Field(
        ge=0,
        nullable=True,
        alias="limits_market.max",
        title="Max Market Size",
        description="Maximum market order size",
    )

    # Limits - Leverage (only 3/19)
    limits_leverage_min: Optional[Series[float]] = pa.Field(
        ge=0,
        nullable=True,
        alias="limits_leverage.min",
        title="Min Leverage",
        description="Minimum leverage",
    )
    limits_leverage_max: Optional[Series[float]] = pa.Field(
        ge=0,
        nullable=True,
        alias="limits_leverage.max",
        title="Max Leverage",
        description="Maximum leverage",
    )

    # Margin modes (only 5/19 - Binance variants and Bitget)
    marginModes_cross: Optional[Series[bool]] = pa.Field(
        nullable=True, title="Cross Margin", description="Supports cross margin"
    )
    marginModes_isolated: Optional[Series[bool]] = pa.Field(
        nullable=True, title="Isolated Margin", description="Supports isolated margin"
    )

    # Additional rare fields
    index: Optional[Series[str]] = pa.Field(
        nullable=True, title="Index", description="Index identifier"
    )

    # Additional exchange-specific fields allowed via strict=False
    # Examples: id2, uuid, uppercaseId, feeCurrency, tiers_maker, tiers_taker, etc.
