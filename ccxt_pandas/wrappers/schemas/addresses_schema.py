"""Addresses data schema."""

from typing import Optional

import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class AddressesSchema(BaseExchangeSchema):
    """Addresses data schema.

    Used by methods like fetch_deposit_addresses.

    Returns deposit address information for receiving cryptocurrency deposits,
    including network details and optional tags/memos for currencies that require them.
    """

    # Required fields
    currency: Series[str] = pa.Field(title="Currency", description="Currency code")
    network: Series[str] = pa.Field(
        title="Network",
        description="Deposit/withdraw network (e.g., ERC20, TRC20, BSC20)",
    )
    address: Series[str] = pa.Field(
        title="Address", description="Deposit address for the currency"
    )

    # Optional fields
    tag: Optional[Series[str]] = pa.Field(
        nullable=True,
        title="Tag",
        description="Tag/memo/payment ID for currencies that require it (e.g., XRP, XMR)",
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
