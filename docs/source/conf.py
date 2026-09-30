import os
import sys

sys.path.insert(0, os.path.abspath("../../src"))

project = "Colors"
author = "Heriberto Espino Montelongo"
release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
]

autosummary_generate = True
autodoc_member_order = "bysource"
autodoc_typehints = "description"

html_theme = "alabaster"
html_static_path = ["_static"]
html_title = "contrastcolors documentation"
