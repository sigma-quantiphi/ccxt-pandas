"""Base schema classes for all exchange response DataFrames."""


import pandera.pandas as pa
from pandera.typing import Series


class BaseExchangeSchema(pa.DataFrameModel):
    """Shared fields across all exchange responses.

    All schemas inherit from this base class to provide consistent
    exchange and account identifiers across DataFrame responses.
    """

    exchange: Series[str] | None = pa.Field(
        nullable=True, title="Exchange", description="Exchange name"
    )
    account: Series[str] | None = pa.Field(
        nullable=True, title="Account", description="Account identifier"
    )

    class Config:
        """Schema configuration."""

        strict = False  # Allow extra columns (exchange-specific fields)
        coerce = True  # Auto-convert types where possible


class FeeFieldsMixin(pa.DataFrameModel):
    """Mixin for fee-related fields.

    Provides standard fee fields (currency, cost, rate) that can be inherited
    by schemas representing transactions, trades, and orders.
    """

    fee_currency: Series[str] | None = pa.Field(
        nullable=True,
        title="Fee Currency",
        description="Currency in which fee was charged",
    )
    fee_cost: Series[float] | None = pa.Field(
        ge=0, nullable=True, title="Fee Cost", description="Fee amount charged"
    )
    fee_rate: Series[float] | None = pa.Field(
        ge=0,
        nullable=True,
        title="Fee Rate",
        description="Fee rate (approximately fee_cost / amount)",
    )
