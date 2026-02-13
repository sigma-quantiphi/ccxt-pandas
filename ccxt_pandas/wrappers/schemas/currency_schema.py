"""Currency and network data schema."""

from typing import Optional

import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class CurrencySchema(BaseExchangeSchema):
    """Currency data schema with network information.

    Used by methods like fetch_currencies, fetch_deposit_withdraw_fees.

    ID and code are required. Network information is optional as it may
    be expanded into separate rows per network.
    """

    # Core currency fields (required)
    id: Series[str] = pa.Field(
        unique=True, description="Exchange-specific currency ID"
    )
    code: Series[str] = pa.Field(
        description="Unified currency code"
    )
    name: Optional[Series[str]] = pa.Field(
        nullable=True, description="Currency full name"
    )
    active: Optional[Series[bool]] = pa.Field(
        nullable=True, description="Whether currency is active"
    )

    # Network fields (when network info is present)
    network: Optional[Series[str]] = pa.Field(
        nullable=True, description="Network identifier (e.g., ERC20, TRC20)"
    )
    network_fee: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, description="Withdrawal fee on this network"
    )
    network_limits_deposit_min: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, description="Minimum deposit amount"
    )
    network_limits_deposit_max: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, description="Maximum deposit amount"
    )
    network_limits_withdraw_min: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, description="Minimum withdrawal amount"
    )
    network_limits_withdraw_max: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, description="Maximum withdrawal amount"
    )
    network_precision: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, description="Network precision (decimal places)"
    )
    network_deposit: Optional[Series[bool]] = pa.Field(
        nullable=True, description="Whether deposits are enabled"
    )
    network_withdraw: Optional[Series[bool]] = pa.Field(
        nullable=True, description="Whether withdrawals are enabled"
    )

    # Precision fields
    precision: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, description="Currency precision (decimal places)"
    )

    # Fee fields (for deposit_withdraw_fees)
    deposit: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, description="Deposit fee"
    )
    withdraw: Optional[Series[float]] = pa.Field(
        ge=0, nullable=True, description="Withdrawal fee"
    )
