"""Deposit and withdrawal fees data schema."""


import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class DepositWithdrawFeesSchema(BaseExchangeSchema):
    """Deposit and withdrawal fees data schema.

    Used by methods like fetch_deposit_withdraw_fees.

    Returns deposit and withdrawal fee information per currency and network,
    including fixed fees and percentage-based fees.
    """

    # Required fields
    id: Series[str] = pa.Field(title="Currency ID", description="Currency identifier")
    network: Series[str] = pa.Field(
        title="Network", description="Network identifier (e.g., ERC20, TRC20)"
    )
    withdraw_fee: Series[float] = pa.Field(
        ge=0, title="Withdraw Fee", description="Withdrawal fee amount"
    )
    network_withdraw_fee: Series[float] = pa.Field(
        ge=0,
        title="Network Withdraw Fee",
        description="Withdrawal fee for this network",
    )

    # Optional fields (not present in all exchanges)
    network_withdraw_percentage: Series[bool] | None = pa.Field(
        nullable=True,
        title="Network Withdraw Percentage",
        description="Whether network withdrawal fee is percentage-based",
    )
    withdraw_percentage: Series[bool] | None = pa.Field(
        nullable=True,
        title="Withdraw Percentage",
        description="Whether withdrawal fee is percentage-based",
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
