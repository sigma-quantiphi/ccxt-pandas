"""Gate live-API tests behind environment variables.

Tests under `tests/integration/` are scripts that hit real exchanges
(and in some cases place live orders). They are skipped from collection
unless the appropriate env vars are set:

- `CCXT_LIVE=1`        — read-only live API tests
- `CCXT_LIVE_TRADING=1` — order-lifecycle tests (create/edit/cancel real orders)
"""

from __future__ import annotations

import os

_TRADING_FILES = {"test_order_lifecycle_sync.py", "test_order_lifecycle_async.py"}

if not os.getenv("CCXT_LIVE") and not os.getenv("CCXT_LIVE_TRADING"):
    collect_ignore_glob = ["*.py"]
elif not os.getenv("CCXT_LIVE_TRADING"):
    collect_ignore = list(_TRADING_FILES)
