"""ccxt-pandas Explorer — interactive Streamlit dashboard for browsing CCXT methods."""

from pathlib import Path

APP_PATH = Path(__file__).parent / "app.py"
FAVICON_PATH = Path(__file__).parent / "favicon.png"

__all__ = ["APP_PATH", "FAVICON_PATH"]
