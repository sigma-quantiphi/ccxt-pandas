"""Shared pytest fixtures for the unit test suite.

These fixtures build CCXTPandasExchange instances with stub credentials so
HTTP requests can be intercepted by `responses` / `aioresponses` mocks
without ever reaching a live exchange.

Live-API tests live under `tests/integration/` and are gated behind the
`CCXT_LIVE` / `CCXT_LIVE_TRADING` environment variables.
"""

from __future__ import annotations

import ccxt
import pytest

from ccxt_pandas import CCXTPandasExchange


@pytest.fixture
def binance_unauth() -> CCXTPandasExchange:
    """Unauthenticated Binance wrapper for public-endpoint tests."""
    return CCXTPandasExchange(exchange=ccxt.binance({"enableRateLimit": False}))


@pytest.fixture
def binance_authed_stub() -> CCXTPandasExchange:
    """Binance wrapper with stub keys for private-endpoint tests."""
    return CCXTPandasExchange(
        exchange=ccxt.binance(
            {
                "apiKey": "stub-api-key",
                "secret": "stub-api-secret",
                "enableRateLimit": False,
            }
        )
    )


@pytest.fixture
def okx_authed_stub() -> CCXTPandasExchange:
    """OKX wrapper with stub keys for private-endpoint tests."""
    return CCXTPandasExchange(
        exchange=ccxt.okx(
            {
                "apiKey": "stub-api-key",
                "secret": "stub-api-secret",
                "password": "stub-password",
                "enableRateLimit": False,
            }
        )
    )


@pytest.fixture
def mocked_responses():
    """Context manager fixture for mocking sync HTTP calls (ccxt sync REST)."""
    import responses

    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def mocked_aioresponses():
    """Context manager fixture for mocking async HTTP calls (ccxt.pro REST)."""
    from aioresponses import aioresponses

    with aioresponses() as m:
        yield m
