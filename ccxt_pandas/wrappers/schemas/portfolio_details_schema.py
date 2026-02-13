"""Portfolio details data schema."""

import pandera.pandas as pa
from pandera.typing import Series

from ccxt_pandas.wrappers.schemas.base_schemas import BaseExchangeSchema


class PortfolioDetailsSchema(BaseExchangeSchema):
    """Portfolio details data schema.

    Used by methods like fetch_portfolio_details.

    Returns detailed portfolio information including balances, holdings,
    P&L, cost basis, and asset allocation.
    """

    # Required fields
    currency: Series[str] = pa.Field(
        title="Currency", description="Currency code"
    )
    available_balance: Series[float] = pa.Field(
        ge=0, title="Available Balance", description="Available balance amount"
    )
    hold_amount: Series[int] = pa.Field(
        ge=0, title="Hold Amount", description="Amount on hold"
    )
    wallet_name: Series[str] = pa.Field(
        title="Wallet Name", description="Wallet name"
    )
    account_id: Series[str] = pa.Field(
        title="Account ID", description="Account identifier"
    )
    account_uuid: Series[str] = pa.Field(
        title="Account UUID", description="Account UUID"
    )
    total_balance_fiat: Series[float] = pa.Field(
        ge=0, title="Total Balance Fiat", description="Total balance in fiat currency"
    )
    total_balance_crypto: Series[float] = pa.Field(
        ge=0, title="Total Balance Crypto", description="Total balance in crypto"
    )
    available_to_trade_fiat: Series[float] = pa.Field(
        ge=0, title="Available to Trade Fiat", description="Available to trade in fiat"
    )
    available_to_trade_crypto: Series[float] = pa.Field(
        ge=0, title="Available to Trade Crypto", description="Available to trade in crypto"
    )
    available_to_transfer_fiat: Series[float] = pa.Field(
        ge=0, title="Available to Transfer Fiat", description="Available to transfer in fiat"
    )
    available_to_transfer_crypto: Series[float] = pa.Field(
        ge=0, title="Available to Transfer Crypto", description="Available to transfer in crypto"
    )
    allocation: Series[float] = pa.Field(
        ge=0, title="Allocation", description="Portfolio allocation percentage"
    )
    cost_basis: Series[float] = pa.Field(
        ge=0, title="Cost Basis", description="Cost basis amount"
    )
    cost_basis_currency: Series[str] = pa.Field(
        title="Cost Basis Currency", description="Currency of cost basis"
    )
    is_cash: Series[bool] = pa.Field(
        title="Is Cash", description="Whether asset is cash"
    )
    average_entry_price: Series[float] = pa.Field(
        ge=0, title="Average Entry Price", description="Average entry price"
    )
    average_entry_price_currency: Series[str] = pa.Field(
        title="Average Entry Price Currency", description="Currency of average entry price"
    )
    asset_uuid: Series[str] = pa.Field(
        title="Asset UUID", description="Asset UUID"
    )
    unrealized_pnl: Series[float] = pa.Field(
        title="Unrealized PnL", description="Unrealized profit and loss"
    )
    asset_color: Series[str] = pa.Field(
        title="Asset Color", description="Asset display color"
    )
    account_type: Series[str] = pa.Field(
        title="Account Type", description="Account type"
    )
    # Note: exchange field comes from BaseExchangeSchema (Optional)
