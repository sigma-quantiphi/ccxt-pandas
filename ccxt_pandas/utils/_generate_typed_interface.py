import inspect
import types as builtin_types
from typing import Callable, Literal, Union, get_args, get_origin

import ccxt
import ccxt.pro as ccxt_pro

from ccxt_pandas.wrappers.method_mappings import (
    dataframe_methods,
    modified_methods,
    get_method_schema,
)

# Build reverse lookup from ccxt.base.types for known type aliases
_CCXT_TYPE_ALIASES: dict[str, str] = {}
try:
    import ccxt.base.types as _ccxt_types

    for _name in dir(_ccxt_types):
        _obj = getattr(_ccxt_types, _name)
        # Only map type aliases (skip classes, functions, modules)
        if _name.startswith("_") or inspect.isclass(_obj) or inspect.isfunction(_obj):
            continue
        _CCXT_TYPE_ALIASES[id(_obj)] = _name
except ImportError:
    pass

# Parameter name overrides: these replace the resolved annotation entirely
_PARAM_OVERRIDES = {
    "symbol": "str | list[str]",
    "code": "str | list[str]",
    "orders": "pd.DataFrame",
}

# Threshold for switching to multi-line signature formatting
_MULTILINE_THRESHOLD = 3


def resolve_annotation(annotation) -> str:
    """Recursively resolve a type annotation to a clean string representation."""
    # Check ccxt type alias lookup first
    alias = _CCXT_TYPE_ALIASES.get(id(annotation))
    if alias:
        return alias

    origin = get_origin(annotation)

    # Handle Union types: typing.Union and PEP 604 types.UnionType
    if origin is Union or isinstance(annotation, builtin_types.UnionType):
        args = get_args(annotation)
        parts = [resolve_annotation(a) for a in args]
        return " | ".join(parts)

    # Handle Literal
    if origin is Literal:
        args = get_args(annotation)
        return f"Literal[{', '.join(repr(a) for a in args)}]"

    # Handle generic types (list[str], dict[str, Any], etc.)
    if origin is not None:
        args = get_args(annotation)
        base = getattr(origin, "__name__", str(origin))
        if args:
            return f"{base}[{', '.join(resolve_annotation(a) for a in args)}]"
        return base

    # Handle NoneType
    if annotation is type(None):
        return "None"

    # Handle plain types
    if hasattr(annotation, "__name__"):
        return annotation.__name__

    return str(annotation)


def get_signature_with_custom_types(
    method: Callable,
    method_name: str,
    is_async: bool = False,
) -> str:
    sig = inspect.signature(method)
    params = []
    tail_params = []  # limit and params go after our injected args
    has_since = "since" in sig.parameters
    has_symbol = "symbol" in sig.parameters or "code" in sig.parameters
    for name, param in sig.parameters.items():
        if name == "self":
            continue
        # Skip `since` — replaced by from_date/to_date
        if name == "since":
            continue
        param_str = name
        if param.annotation != inspect.Parameter.empty:
            if name in _PARAM_OVERRIDES:
                annotation_str = _PARAM_OVERRIDES[name]
            else:
                annotation_str = resolve_annotation(param.annotation)
            param_str += f": {annotation_str}"
        if param.default is not inspect.Parameter.empty:
            param_str += f" = {param.default!r}"
        # Hold limit and params aside so from_date/to_date/cache come first
        if name in ("limit", "params"):
            tail_params.append(param_str)
        else:
            params.append(param_str)
    # Add from_date/to_date for methods that support since
    if has_since:
        params.append("from_date: pd.Timestamp | dict | str | None = None")
        params.append("to_date: pd.Timestamp | dict | str | None = None")
    # Add cache for methods with symbol/code support and since
    if has_symbol and has_since:
        params.append("cache: bool = False")
    params.extend(tail_params)

    # Determine return type - use Pandera schema types if available
    if method_name in dataframe_methods:
        schema = get_method_schema(method_name)
        if schema:
            base_type = f"DataFrame[{schema.__name__}]"
        else:
            base_type = "pd.DataFrame"
    else:
        base_type = "dict"

    if is_async:
        return_type = f"Awaitable[{base_type}] | list[Awaitable[{base_type}]]"
    else:
        return_type = base_type

    # Format signature
    all_params = ["self"] + params
    if len(all_params) > _MULTILINE_THRESHOLD + 1:  # +1 for self
        # Multi-line format
        param_lines = ",\n        ".join(all_params)
        return (
            f"\n    def {method_name}(\n"
            f"        {param_lines},\n"
            f"    ) -> {return_type}:\n"
            f'        """Returns a {base_type} from ccxt.{method_name}"""\n'
            f"        ..."
        )
    else:
        # Single-line format
        param_str = ", ".join(all_params)
        return (
            f"\n    def {method_name}({param_str}) -> {return_type}:\n"
            f'        """Returns a {base_type} from ccxt.{method_name}"""\n'
            f"        ..."
        )


def _collect_used_imports(code: str) -> str:
    """Emit only the imports actually referenced in the generated code."""
    typing_imports = ["Protocol"]
    if "Literal[" in code:
        typing_imports.append("Literal")
    if "Awaitable[" in code:
        typing_imports.append("Awaitable")
    lines = [f"from typing import {', '.join(sorted(typing_imports))}"]
    if "Decimal" in code:
        lines.append("from decimal import Decimal")
    # ccxt type imports
    ccxt_types = []
    for alias in sorted(set(_CCXT_TYPE_ALIASES.values())):
        if alias in code:
            ccxt_types.append(alias)
    if ccxt_types:
        lines.append(f"from ccxt.base.types import {', '.join(ccxt_types)}")

    # Pandera imports - only if DataFrame[Schema] is used
    if "DataFrame[" in code:
        lines.append("from pandera.typing import DataFrame")

        # Collect all schema names used
        import re

        schema_pattern = r"DataFrame\[(\w+)\]"
        schemas = sorted(set(re.findall(schema_pattern, code)))
        if schemas:
            # Import all used schemas
            lines.append(f"from ccxt_pandas.wrappers.schemas import (")
            for i, schema in enumerate(schemas):
                comma = "," if i < len(schemas) - 1 else ""
                lines.append(f"    {schema}{comma}")
            lines.append(")")

    lines.append("import pandas as pd")
    return "\n".join(lines) + "\n"


def generate_typed_interface_class(
    base: type,
    class_name: str,
    is_async: bool = False,
) -> str:
    class_header = (
        f"\nclass {class_name}(Protocol):\n"
        f'    """A Class to add type hinting to {class_name}"""\n'
    )
    lines = []
    for method_name in sorted(modified_methods):
        if hasattr(base, method_name):
            method = getattr(base, method_name)
            try:
                stub = get_signature_with_custom_types(
                    method,
                    method_name,
                    is_async=is_async,
                )
                lines.append(stub)
            except Exception as e:
                print(f"Error inspecting {method_name}: {e}")
    body = class_header + "\n".join(lines) + "\n"
    import_lines = _collect_used_imports(body)
    return import_lines + body


if __name__ == "__main__":
    sync_code = generate_typed_interface_class(ccxt.Exchange, "CCXTPandasExchangeTyped")
    async_code = generate_typed_interface_class(
        ccxt_pro.Exchange,
        "AsyncCCXTPandasExchangeTyped",
        is_async=True,
    )
    with open("ccxt_pandas/utils/ccxt_pandas_exchange_typed.py", "w") as f:
        f.write(sync_code)
    with open("ccxt_pandas/utils/async_ccxt_pandas_exchange_typed.py", "w") as f:
        f.write(async_code)
    print("Generated both typed interface files.")
