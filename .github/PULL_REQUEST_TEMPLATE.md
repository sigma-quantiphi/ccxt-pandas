## Summary

<!-- What does this change and why? Link the issue it closes. -->

## Checklist

- [ ] Tests cover the change.
- [ ] `ruff check` and `ruff format --check` pass.
- [ ] `mypy ccxt_pandas` passes.
- [ ] Pandera schema updated if a return DataFrame shape changed.
- [ ] Typed stubs regenerated (`uv run python ccxt_pandas/utils/_generate_typed_interface.py`) if a new method was added.
- [ ] `CHANGELOG.md` updated under `[Unreleased]`.

## Screenshots / output

<!-- Optional: DataFrame output, dashboard screenshot, CI run link. -->
