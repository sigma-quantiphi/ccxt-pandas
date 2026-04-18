import inspect
from importlib.metadata import version
from pathlib import Path

import ccxt
import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image

from ccxt_pandas import CCXTPandasExchange

FAVICON_PATH = Path(__file__).parent / "favicon.png"

favicon = Image.open(FAVICON_PATH)
st.set_page_config(layout="wide", page_title="CCXT Explorer", page_icon=favicon)
plot_types = ["line", "bar", "scatter"]
agg_funcs = ["None", "mean", "sum", "min", "max", "count", "nunique"]

st.title("CCXT Explorer")
st.subheader(f"ccxt: {version('ccxt')} | ccxt-pandas: {version('ccxt_pandas')}")
st.sidebar.image(favicon)
st.sidebar.markdown("[Made by Sigma Quantiphi](https://sigmaquantiphi.com)")
st.sidebar.markdown(
    """
    <a href="https://www.youtube.com/@sigmaquantiphi" target="_blank" style="text-decoration: none; display: inline-flex; align-items: center;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/0/09/YouTube_full-color_icon_(2017).svg" alt="YouTube" width="20" style="margin-right: 8px;">
        <span style="font-size: 18px;">Tutorials on YouTube</span>
    </a>
    """,
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    """
    <a href="https://github.com/sigma-quantiphi" target="_blank" style="text-decoration: none; display: inline-flex; align-items: center; margin-top: 10px;">
        <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub" width="24" style="margin-right: 10px;">
        <span style="font-size: 18px;">View on GitHub</span>
    </a>
    """,
    unsafe_allow_html=True,
)

exchange_id = st.sidebar.selectbox(
    "Exchange", ccxt.exchanges, index=ccxt.exchanges.index("binance")
)

exchange_class = getattr(ccxt, exchange_id)
init_exchange = exchange_class()
default_types = [x for x in ["spot", "future", "swap", "option"] if init_exchange.has[x]]
default_type = st.sidebar.selectbox("Default Type", default_types, index=0)
default_sub_type = st.sidebar.selectbox(
    "Default Sub Type",
    ["linear", "inverse"],
    index=0,
    help="Linear for USD-M and inverse for COIN-M",
)
has_sandbox_mode = init_exchange.has["sandbox"]
if has_sandbox_mode:
    sandox_mode = st.sidebar.toggle("Set to sandbox mode", value=False)
else:
    sandox_mode = False
is_option = default_type == "option"
secrets = {k: v for k, v in init_exchange.requiredCredentials.items() if v}
for k in secrets:
    secrets[k] = st.sidebar.text_input(k, type="password")
secrets = {k: v for k, v in secrets.items() if v}
exchange = exchange_class(
    {
        **secrets,
        "enableRateLimit": True,
        "options": {
            "defaultType": default_type,
            "defaultSubType": default_sub_type,
            "loadAllOptions": True,
        },
    }
)
exchange.set_sandbox_mode(sandox_mode)
pandas_exchange = CCXTPandasExchange(exchange)


@st.cache_data(ttl=3600, max_entries=10)
def fetch_markets(settings: dict) -> pd.DataFrame:
    print(settings)
    return pandas_exchange.load_markets()


markets = fetch_markets(
    settings={
        "exchange_id": exchange_id,
        "sandbox_mode": sandox_mode,
        "defaultType": default_type,
        "defaultSubType": default_sub_type,
    }
)
if "markets" not in st.session_state or not markets.equals(st.session_state.markets):
    st.session_state.markets = markets

method_signatures = {}
for name, method in inspect.getmembers(exchange, predicate=inspect.ismethod):
    if name in exchange.has and exchange.has[name] and name.startswith("fetch"):
        sig = inspect.signature(method)
        method_signatures[name] = sig
method_names = list(method_signatures.keys())
if "fetchOHLCV" in method_names:
    default_method = method_names.index("fetchOHLCV")
elif "fetchTrades" in method_names:
    default_method = method_names.index("fetchTrades")
elif "fetchOrderBook" in method_names:
    default_method = method_names.index("fetchOrderBook")
else:
    default_method = 0
selected_method = st.sidebar.selectbox("Choose a method", method_names, index=default_method)
sig = method_signatures.get(selected_method)

st.subheader(f"Symbols on {exchange_id}")
call_args = {}
selected_symbols = []

if sig:
    param_names = [p.name for p in sig.parameters.values()]
    if "symbols" in param_names:
        selection = ["multi-row"]
    elif "symbol" in param_names:
        selection = ["single-row"]
    else:
        selection = []
    event = st.dataframe(
        st.session_state.markets.set_index("symbol"),
        key="data",
        on_select="rerun",
        selection_mode=selection,
    )
    if event.selection.rows:
        selected_symbols = st.session_state.markets.loc[event.selection.rows, "symbol"].tolist()
    else:
        selected_symbols = None
    if "symbols" in param_names:
        call_args["symbols"] = selected_symbols
    elif "symbol" in param_names and selected_symbols:
        call_args["symbol"] = selected_symbols[0]
    if "timeframe" in param_names:
        timeframe_options = ["1m", "5m", "15m", "1h", "6h", "12h", "1d"]
        selected_timeframe = st.sidebar.selectbox("Timeframe", timeframe_options)
        call_args["timeframe"] = selected_timeframe
    if "since" in param_names:
        selected_since = st.sidebar.date_input(
            "Start time", value=pd.Timestamp.now(tz="UTC"), help="First Data & Time"
        )
        call_args["since"] = pd.Timestamp(selected_since, tz="UTC")
    if "limit" in param_names:
        selected_limit = st.sidebar.number_input(
            "Limit", value=1000, max_value=10000, help="Number of datapoints."
        )
        call_args["limit"] = selected_limit

if sig:
    for _i, param in enumerate(sig.parameters.values()):
        if param.name not in ["symbol", "symbols", "timeframe", "since", "limit"]:
            if param.default is inspect.Parameter.empty:
                call_args[param.name] = ""
            else:
                call_args[param.name] = param.default
secrets_text = "".join(f'\n    "{k}": {v},' for k, v in secrets.items())
code_snippet = f"""
import ccxt
from ccxt_pandas import CCXTPandasExchange

exchange = ccxt.{exchange_id}({{{secrets_text}
    "options": {{
        "defaultType": "{default_type}",
        "defaultSubType": "{default_sub_type}",
        "loadAllOptions": {is_option},
    }},
}})
"""
if sandox_mode:
    code_snippet += """exchange.set_sandbox_mode(True)
"""
code_snippet += f"""pandas_exchange = CCXTPandasExchange(exchange=exchange)
result = pandas_exchange.{selected_method}(**{call_args})
print(result)"""
st.subheader("Code Snippet")
st.code(code_snippet, language="python")

st.subheader("Data")
try:
    method_to_call = getattr(pandas_exchange, selected_method)
    result = method_to_call(**call_args)
    if isinstance(result, pd.DataFrame):
        if "symbol" in result.columns:
            result = result.merge(
                markets.reindex(
                    columns=[
                        "symbol",
                        "base",
                        "quote",
                        "settle",
                        "type",
                        "subType",
                        "underlying",
                        "strike",
                        "optionType",
                        "expiryDatetime",
                        "contractSize",
                        "active",
                    ]
                )
            ).dropna(axis=1)
        if not result.empty:
            st.dataframe(result.set_index("symbol"))
            st.subheader("Plotting")
            if "timestamp" in result.columns:
                default_x = "timestamp"
                default_plot = "line"
            else:
                default_x = "symbol"
                default_plot = "bar"
            if "price" in result.columns:
                default_y = "price"
            elif "qty" in result.columns:
                default_y = "qty"
            elif "close" in result.columns:
                default_y = "close"
            else:
                default_y = result.columns[1]
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                plot_type = st.selectbox(
                    "Plot Type", plot_types, index=plot_types.index(default_plot)
                )
                agg_func = st.selectbox("Aggregation", agg_funcs, index=0)
            with col2:
                x_axis = st.selectbox(
                    "X Axis",
                    result.columns,
                    index=result.columns.tolist().index(default_x),
                )
                facet_row = st.selectbox(
                    "Facet Row (optional)", ["None"] + list(result.columns), index=0
                )
            with col3:
                y_axis = st.selectbox(
                    "Y Axis",
                    result.columns,
                    index=result.columns.tolist().index(default_y),
                )
                facet_col = st.selectbox(
                    "Facet Col (optional)", ["None"] + list(result.columns), index=0
                )
            with col4:
                color = st.selectbox(
                    "Color (optional)", ["None"] + result.columns.tolist(), index=0
                )
                size = None
                if plot_type == "scatter":
                    size = st.selectbox("Size (optional)", ["None"] + list(result.columns), index=0)

            plot_data = result.copy()
            if agg_func != "None":
                group_cols = [x_axis]
                if facet_row != "None":
                    group_cols.append(facet_row)
                if facet_col != "None":
                    group_cols.append(facet_col)
                if color != "None":
                    group_cols.append(color)
                if plot_type == "scatter" and size != "None":
                    group_cols.append(size)

                agg_dict = {y_axis: agg_func}
                plot_data = plot_data.groupby(group_cols, dropna=False).agg(agg_dict).reset_index()

            plot_kwargs = {
                "x": x_axis,
                "y": y_axis,
                "title": f"{plot_type.capitalize()} Plot of {y_axis} vs {x_axis}",
                "height": 600,
            }
            if color != "None":
                plot_kwargs["color"] = color
            if facet_row != "None":
                plot_kwargs["facet_row"] = facet_row
            if facet_col != "None":
                plot_kwargs["facet_col"] = facet_col
            if plot_type == "scatter" and size != "None":
                plot_kwargs["size"] = size
            try:
                fig = getattr(px, plot_type)(plot_data, **plot_kwargs)
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error generating plot: {e}")
    else:
        st.write(result)
except Exception as e:
    if "missing 1 required positional argument: 'symbol'" in str(e):
        st.error("Please select a symbol from the table first.")
    else:
        st.error(f"Error executing method: {e}")
