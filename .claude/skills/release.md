---
name: release
description: Cut a new release of ccxt-pandas. Run all checks, bump the version in pyproject.toml, update CHANGELOG.md, commit, then push and create a GitHub Release (publish.yml takes care of PyPI). Use when the user asks to "release", "publish", "cut a version", or "ship X.Y.Z".
---

# Release

## Required input

- **Version bump**: `patch` (0.14.0 → 0.14.1), `minor` (0.14.0 → 0.15.0), or `major` (0.14.0 → 1.0.0)
- OR an **explicit version** string

If unspecified, ask the user.

## Steps

### 1. Determine the new version

Read the current `version` from `pyproject.toml` (`[project] version = …`). Calculate the new version.

### 2. Run validation

Run all checks; **stop and fix** if any fail:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy ccxt_pandas
uv run pytest tests/ -v
uv run python -c "from ccxt_pandas import CCXTPandasExchange, AsyncCCXTPandasExchange, OHLCVSchema, CCXTPandasError"
uv run python -c "from ccxt_pandas_mcp.server import mcp"
uv run python -c "from ccxt_pandas_explorer import APP_PATH"
```

### 3. Update CHANGELOG.md

Move items from `## Unreleased` into a new `## [X.Y.Z] - YYYY-MM-DD` section (Keep a Changelog format). Leave `## Unreleased` empty for the next cycle.

### 4. Verify CLAUDE.md is current

If this release added new packages, schemas, or workflows, make sure CLAUDE.md reflects them.

### 5. Commit

```
Release vX.Y.Z
```

Include only `CHANGELOG.md` and any incidental fixes from step 2. The version is derived from the git tag by `hatch-vcs` — there is no version field to edit.

### 6. Tag and push

```bash
git push
git tag vX.Y.Z
git push --tags
```

### 7. Create the GitHub Release

```bash
gh release create vX.Y.Z --title "vX.Y.Z" --notes-from-tag
```

Or via the web UI. `publish.yml` runs on `release: published` and pushes to PyPI with sigstore attestations.

### 9. Report

Tell the user:
- The new version
- Which checks passed
- The release URL
