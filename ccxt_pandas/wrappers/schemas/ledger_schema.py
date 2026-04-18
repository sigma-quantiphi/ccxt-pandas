"""Ledger data schema."""

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema, FeeFieldsMixin


class LedgerSchema(BaseExchangeSchema, FeeFieldsMixin):
    """Ledger data schema.

    Used by methods like fetch_ledger.

    Returns ledger entries showing account balance changes from trades,
    deposits, withdrawals, and other transactions.
    """

    # Required fields
    id: Series[str] = pa.Field(title="ID", description="Ledger entry identifier (e.g., order ID)")
    direction: Series[str] = pa.Field(
        isin=["in", "out"], title="Direction", description="Direction: 'in' or 'out'"
    )
    account: Series[str] = pa.Field(title="Account", description="Account identifier")
    referenceId: Series[str] = pa.Field(
        title="Reference ID", description="ID of trade, transaction, etc."
    )
    referenceAccount: Series[str] = pa.Field(
        title="Reference Account", description="ID of opposite account"
    )
    type: Series[str] = pa.Field(
        title="Type", description="Reference type (e.g., trade, deposit, withdrawal)"
    )
    currency: Series[str] = pa.Field(title="Currency", description="Currency code")
    amount: Series[float] = pa.Field(ge=0, title="Amount", description="Amount (excluding fee)")
    timestamp: Series[pd.Timestamp] = pa.Field(
        title="Timestamp", description="Ledger entry timestamp"
    )
    datetime: Series[pd.Timestamp] = pa.Field(
        title="Datetime", description="Ledger entry datetime (alias)"
    )
    before: Series[float] = pa.Field(ge=0, title="Before", description="Balance before this entry")
    after: Series[float] = pa.Field(ge=0, title="After", description="Balance after this entry")
    status: Series[str] = pa.Field(
        isin=["ok", "pending", "canceled"],
        title="Status",
        description="Entry status",
    )
    # Note: fee_currency, fee_cost, fee_rate come from FeeFieldsMixin (Optional)
    # Note: exchange field comes from BaseExchangeSchema (Optional)
