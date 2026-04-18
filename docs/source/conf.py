"""Sphinx configuration for ccxt-pandas."""

import datetime
import os
import sys
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version

sys.path.insert(0, os.path.abspath("../../"))

project = "ccxt-pandas"
copyright = f"{datetime.datetime.now().year}, Sigma Quantiphi"
author = "Sigma Quantiphi"

try:
    release = _pkg_version("ccxt-pandas")
except PackageNotFoundError:
    release = "0.0.0+unknown"

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_sitemap",
    "sphinxext.opengraph",
]
source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
autosummary_generate = True
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "inherited-members": False,
}
autodoc_mock_imports = [
    "fastmcp",
    "streamlit",
    "plotly",
    "PIL",
]
myst_enable_extensions = ["colon_fence", "deflist", "linkify", "tasklist"]
myst_heading_anchors = 3

# README contains relative links to examples/*.py and other repo paths that
# don't resolve inside the docs tree — they work fine on GitHub. Stop MyST
# from treating them as broken cross-references.
# `ref.python` covers schema attribute names (`type`, `id`) that exist on
# multiple re-exported schemas — Sphinx flags ambiguity but the right target
# is unimportant for class-level docs.
suppress_warnings = [
    "myst.xref_missing",
    "ref.python",
    "app.add_object",  # pandera DataFrameModel.Config shows once per subclass
    "autosectionlabel.*",
]

templates_path = ["_templates"]
exclude_patterns = []

html_baseurl = "https://sigma-quantiphi.github.io/ccxt-pandas/"
html_theme = "furo"
html_static_path = ["_static"]
html_context = {"default_mode": "dark"}
html_logo = "_static/Sigma-Quantiphi-logo-new.png"
html_favicon = "_static/favicon.png"
html_theme_options = {
    "source_repository": "https://github.com/sigma-quantiphi/ccxt-pandas/",
    "source_branch": "main",
    "source_directory": "docs/source/",
}
ogp_site_url = html_baseurl
ogp_site_name = "ccxt-pandas docs"
ogp_description_length = 180
