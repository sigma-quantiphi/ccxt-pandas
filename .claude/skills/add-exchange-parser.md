---
name: add-exchange-parser
description: Procedure for handling an exchange-specific response shape that doesn't conform to CCXT's unified format (e.g. Binance's account/withdraw history, Bybit's instruments-info). Use when an implicit method (one not listed in method_mappings) needs to return a DataFrame, or when an exchange-specific quirk requires custom field-type coercion.
---

# Add an exchange-specific parser

Implicit methods — CCXT methods like `sapi_get_capital_config_getall` that aren't in `method_mappings.modified_methods` — get intercepted by `__getattribute__` and routed through the registry in `ccxt_pandas/wrappers/exchange_parsers.py`.

## Required input

- The exchange ID (e.g. `binance`, `okx`, `bybit`).
- The CCXT method name in **camelCase** (e.g. `sapiGetCapitalConfigGetall`).
- One example response payload.

## Steps

### 1. Register the parser config

Open `ccxt_pandas/wrappers/exchange_parsers.py`. Find the section for your exchange (`BINANCE_PARSERS`, `OKX_PARSERS`, …) and add an entry keyed by camelCase method name:

```python
"sapiGetCapitalConfigGetall": {
    "response_path": None,            # or "data.list" if the rows are nested
    "is_list": True,                  # True if response is a list, False for single object
    "expand_dict_columns": ["networkList"],  # JSON columns to explode if any
    "rename_columns": {"coin": "currency"},  # optional renames
},
```

`_build_dual_case_config()` auto-generates the snake_case alias (e.g. `sapi_get_capital_config_getall`) at import time using `exchange.un_camel_case()`. Don't add both forms manually.

### 2. Field types

If the response uses fields that aren't in CCXT's unified vocabulary, edit `ccxt_pandas/wrappers/field_type_mappings.py` to register the relevant exchange-specific field set:

```python
BINANCE_NUMERIC_FIELDS |= {"withdrawFee", "minWithdrawAmount", "maxWithdrawAmount"}
BINANCE_BOOL_FIELDS    |= {"withdrawEnable", "depositEnable"}
```

The field-type maps drive the post-conversion dtype coercion in `BaseProcessor`.

### 3. Add a unit test

```python
def test_binance_capital_config(binance_authed_stub, mocked_responses):
    mocked_responses.add(
        "GET",
        "https://api.binance.com/sapi/v1/capital/config/getall",
        json=[{"coin": "BTC", "withdrawFee": "0.0005", "withdrawEnable": True}],
    )
    df = binance_authed_stub.sapi_get_capital_config_getall()
    assert df["withdrawFee"].dtype == "float64"
    assert df["withdrawEnable"].dtype == "bool"
```

### 4. Verify

```bash
uv run ruff format . && uv run ruff check . --fix
uv run pytest tests/test_<your_test>.py -v
```

### 5. Document

If this is a substantial new exchange surface, mention the parser group in CLAUDE.md under "Exchange parsers (ccxt_pandas/wrappers/exchange_parsers.py)".
