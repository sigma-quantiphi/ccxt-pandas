"""Accounts data schema."""

import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class AccountsSchema(BaseExchangeSchema):
    """Accounts data schema.

    Used by methods like fetch_accounts.

    Returns user account information including account ID and type,
    often used for subaccount management.
    """

    # Required fields
    id: Series[str] = pa.Field(title="Account ID", description="Account identifier")
    type: Series[str] = pa.Field(title="Type", description="Account type")
    # Note: exchange field comes from BaseExchangeSchema (Optional)
