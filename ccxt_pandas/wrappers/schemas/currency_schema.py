"""Currency and network data schema."""


import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class CurrencySchema(BaseExchangeSchema):
    """Currency data schema with network information.

    Used by methods like fetch_currencies, fetch_deposit_withdraw_fees.

    Returns currency information including deposit/withdrawal capabilities
    and network-specific details.
    """

    # Required fields
    id: Series[str] = pa.Field(
        unique=True, title="Currency ID", description="Exchange-specific currency ID"
    )
    code: Series[str] = pa.Field(
        title="Currency Code", description="Unified currency code (e.g., BTC, ETH)"
    )
    precision: Series[float] = pa.Field(
        ge=0, title="Precision", description="Currency precision (decimal places)"
    )
    type: Series[str] = pa.Field(title="Type", description="Currency type")
    name: Series[str] = pa.Field(title="Name", description="Currency full name")
    network: Series[str] = pa.Field(
        title="Network", description="Network identifier (e.g., ERC20, TRC20, BEP20)"
    )
    network_id: Series[str] = pa.Field(
        title="Network ID", description="Exchange-specific network identifier"
    )
    network_precision: Series[float] = pa.Field(
        ge=0,
        title="Network Precision",
        description="Network precision (decimal places)",
    )

    # Optional boolean fields
    active: Series[bool] | None = pa.Field(
        nullable=True,
        title="Active",
        description="Whether currency is active for trading",
    )
    deposit: Series[bool] | None = pa.Field(
        nullable=True,
        title="Deposit Enabled",
        description="Whether deposits are enabled",
    )
    withdraw: Series[bool] | None = pa.Field(
        nullable=True,
        title="Withdraw Enabled",
        description="Whether withdrawals are enabled",
    )
    network_deposit: Series[bool] | None = pa.Field(
        nullable=True,
        title="Network Deposit Enabled",
        description="Whether deposits are enabled on this network",
    )
    network_withdraw: Series[bool] | None = pa.Field(
        nullable=True,
        title="Network Withdraw Enabled",
        description="Whether withdrawals are enabled on this network",
    )
    network_active: Series[bool] | None = pa.Field(
        nullable=True, title="Network Active", description="Whether network is active"
    )

    # Optional fee fields
    fee: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Fee", description="General fee amount"
    )
    network_fee: Series[float] | None = pa.Field(
        ge=0,
        nullable=True,
        title="Network Fee",
        description="Withdrawal fee on this network",
    )

    # Optional limits fields
    limits_withdraw_min: Series[float] | None = pa.Field(
        ge=0,
        nullable=True,
        title="Withdraw Min",
        description="Minimum withdrawal amount",
    )
    limits_deposit_min: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Deposit Min", description="Minimum deposit amount"
    )
    network_limits_deposit_min: Series[float] | None = pa.Field(
        ge=0,
        nullable=True,
        title="Network Deposit Min",
        description="Minimum deposit amount on this network",
    )
    network_limits_withdraw_min: Series[float] | None = pa.Field(
        ge=0,
        nullable=True,
        title="Network Withdraw Min",
        description="Minimum withdrawal amount on this network",
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
