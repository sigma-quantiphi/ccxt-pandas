"""Transactions data schema."""

from typing import Optional

import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema, FeeFieldsMixin


class TransactionsSchema(BaseExchangeSchema, FeeFieldsMixin):
    """Transactions data schema.

    Used by methods like fetch_deposits, fetch_withdrawals, fetch_deposits_withdrawals.

    Returns transaction history for deposits and withdrawals including addresses,
    amounts, fees, and transaction status.
    """

    # Required fields
    id: Series[str] = pa.Field(
        title="ID", description="Exchange-specific transaction ID"
    )
    txid: Series[str] = pa.Field(
        title="TXID", description="Transaction hash on blockchain"
    )
    timestamp: Series[pd.Timestamp] = pa.Field(
        title="Timestamp", description="Transaction timestamp"
    )
    datetime: Series[pd.Timestamp] = pa.Field(
        title="Datetime", description="Transaction datetime (alias)"
    )
    type: Series[str] = pa.Field(
        isin=["deposit", "withdrawal"],
        title="Type",
        description="Transaction type: 'deposit' or 'withdrawal'",
    )
    amount: Series[float] = pa.Field(
        ge=0, title="Amount", description="Transaction amount (excluding fee)"
    )
    currency: Series[str] = pa.Field(title="Currency", description="Currency code")
    status: Series[str] = pa.Field(
        isin=["ok", "failed", "canceled", "pending"],
        title="Status",
        description="Transaction status",
    )

    # Optional fields
    addressFrom: Optional[Series[str]] = pa.Field(
        nullable=True, title="Address From", description="Sender address"
    )
    address: Optional[Series[str]] = pa.Field(
        nullable=True, title="Address", description="From or to address"
    )
    addressTo: Optional[Series[str]] = pa.Field(
        nullable=True, title="Address To", description="Receiver address"
    )
    tagFrom: Optional[Series[str]] = pa.Field(
        nullable=True, title="Tag From", description="Tag/memo/payment_id for sender"
    )
    tag: Optional[Series[str]] = pa.Field(
        nullable=True, title="Tag", description="Tag/memo/payment_id for address"
    )
    tagTo: Optional[Series[str]] = pa.Field(
        nullable=True, title="Tag To", description="Tag/memo/payment_id for receiver"
    )
    updated: Optional[Series[pd.Timestamp]] = pa.Field(
        nullable=True,
        title="Updated",
        description="Timestamp of most recent status change",
    )
    comment: Optional[Series[str]] = pa.Field(
        nullable=True, title="Comment", description="User-defined comment or message"
    )
    # Note: fee_currency, fee_cost, fee_rate come from FeeFieldsMixin (Optional)
    # Note: exchange field comes from BaseExchangeSchema (Optional)
