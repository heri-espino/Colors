import os
import sys

sys.path.insert(0, os.path.abspath("../../src"))

project = "Colors"
author = "Heriberto Espino Montelongo"
release = "0.1.0"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx.ext.mathjax"]
html_theme = "alabaster"
html_static_path = ["_static"]
