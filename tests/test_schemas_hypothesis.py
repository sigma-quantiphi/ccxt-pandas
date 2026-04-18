"""Hypothesis-driven round-trip test for every Pandera schema.

Generates synthetic frames matching each schema's strategy, then validates
those frames against the schema. Catches dtype-strategy mismatches that
hand-written fixtures miss.
"""

from __future__ import annotations

import inspect

import pandera.pandas as pa
import pytest

from ccxt_pandas.wrappers import schemas as schema_module

# Discover every concrete DataFrameModel exported from the schemas package.
_SCHEMAS = [
    cls
    for _, cls in inspect.getmembers(schema_module, inspect.isclass)
    if issubclass(cls, pa.DataFrameModel) and cls is not pa.DataFrameModel
]


@pytest.mark.parametrize("schema_cls", _SCHEMAS, ids=lambda c: c.__name__)
def test_schema_strategy_roundtrip(schema_cls):
    """Each schema's hypothesis strategy must produce a frame the schema accepts."""
    try:
        example = schema_cls.to_schema().strategy(size=3).example()
    except (NotImplementedError, pa.errors.SchemaDefinitionError, TypeError) as e:
        # TypeError covers schemas with non-generatable column dtypes (dict, custom objects).
        pytest.skip(f"{schema_cls.__name__}: strategy not supported ({e})")
    schema_cls.validate(example, lazy=True)
