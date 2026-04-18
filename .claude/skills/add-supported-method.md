---
name: add-supported-method
description: Procedure for adding a new CCXT method to the ccxt-pandas DataFrame conversion pipeline. Use this when CCXT exposes a new method (or you discover an existing one isn't intercepted) and you want it to return a DataFrame with the standard ccxt-pandas treatment (timestamp coercion, schema validation, snake/camelCase aliasing).
---

# Add a supported CCXT method

A "supported method" is a CCXT method that ccxt-pandas's `__getattribute__` interception routes through `BaseProcessor` so the response comes back as a DataFrame with the right dtypes.

## Required input

- The CCXT method name (snake_case, e.g. `fetch_open_interest_history`).
- One example response — either a docstring snippet from CCXT, a recorded JSON fixture, or a one-off live call dumped to disk.

## Steps

### 1. Pick the response category

Open `ccxt_pandas/wrappers/method_mappings.py` and find the set that matches the response shape:

| Set | Use when |
|---|---|
| `standard_methods` | List-of-dicts that flatten to one DataFrame (most fetch_* methods) |
| `markets_methods` | `load_markets` / `fetch_markets` shape |
| `currencies_methods` | `fetch_currencies` shape (dict keyed by currency code) |
| `balance_methods` | `fetch_balance` (free/used/total per currency) |
| `ohlcv_methods` | `[ts, o, h, l, c, v]` rows |
| `orderbook_methods` | `{bids: [[price, qty], …], asks: [[price, qty], …]}` |
| `orders_methods` | Order create/edit/cancel responses |
| `dict_methods` | Single-dict response that should be coerced to a 1-row DataFrame |

Add the snake_case method name to that set. The camelCase alias is generated automatically by `add_camel_case_methods`.

### 2. Add or extend a Pandera schema

Look under `ccxt_pandas/wrappers/schemas/` for an existing schema that fits the response columns. If one exists, add the new fields. If not:

1. Create a new file `<method>_schema.py` in `ccxt_pandas/wrappers/schemas/`.
2. Subclass `BaseExchangeSchema` (and `FeeFieldsMixin` if the response has fees).
3. List columns with their pandera types (`pa.typing.Series[pd.Timestamp]`, etc.).
4. Re-export from `ccxt_pandas/wrappers/schemas/__init__.py`.
5. Re-export from `ccxt_pandas/__init__.py` and add to `__all__`.

### 3. Wire the schema in

In `ccxt_pandas/wrappers/method_mappings.py`, register the schema in `METHOD_SCHEMAS` so `validate_schemas=True` users get validation.

### 4. Field types (only if novel)

If the new response introduces fields with non-standard types (a numeric field that arrives as a string, a bool that arrives as 0/1, a timestamp not in milliseconds), edit `ccxt_pandas/wrappers/field_type_mappings.py` to register the column under `numeric_fields`, `bool_fields`, or `datetime_fields` for the relevant exchange.

### 5. Regenerate typed stubs

```bash
uv run python ccxt_pandas/utils/_generate_typed_interface.py
```

This rewrites `ccxt_pandas/utils/ccxt_pandas_exchange_typed.py` and `async_ccxt_pandas_exchange_typed.py`. Commit the diff.

### 6. Add a unit test

Create `tests/test_<method>.py` (or extend an existing topic file). Use the `binance_unauth` fixture from `tests/conftest.py` plus `mocked_responses` to stub the HTTP call:

```python
def test_my_method(binance_unauth, mocked_responses):
    mocked_responses.add(
        "GET",
        "https://api.binance.com/api/v3/<endpoint>",
        json=[{...}, {...}],
    )
    df = binance_unauth.fetch_my_method(symbol="BTC/USDT")
    assert list(df.columns) == ["timestamp", "symbol", "..."]
    assert df["timestamp"].dtype == "datetime64[ns, UTC]"
```

### 7. Verify

```bash
uv run ruff format .
uv run ruff check . --fix
uv run mypy ccxt_pandas
uv run pytest tests/ -v
```

### 8. Update CLAUDE.md

If the new method category required a new schema file or a new field-type entry, mention the change in CLAUDE.md so future sessions find it.
