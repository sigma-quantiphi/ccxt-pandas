"""Console-script entry point: `ccxt-pandas-explorer` runs the Streamlit app."""

import sys

from streamlit.web import cli as stcli

from ccxt_pandas_explorer import APP_PATH


def main() -> None:
    sys.argv = ["streamlit", "run", str(APP_PATH), *sys.argv[1:]]
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
