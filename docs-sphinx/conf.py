import os
import sys

# Tell Sphinx where your source code lives
sys.path.insert(0, os.path.abspath("../generated"))

extensions = [
    "sphinx.ext.autodoc",  # Core library for pulling in docstrings
    "sphinx.ext.napoleon",  # Support for Google/NumPy style docstrings
    "sphinx_markdown_builder",  # The magic piece that allows MD output
]

# Basic settings
master_doc = "index"
project = "Camunda Orchestration SDK"

# HTML theme settings - enable table of contents in sidebar
html_theme = "alabaster"
html_theme_options = {
    "sidebar_collapse": True,
    "show_powered_by": False,
}

# Show table of contents in sidebar
html_sidebars = {
    "**": [
        "about.html",
        "searchbox.html",
        "localtoc.html",  # This adds the local table of contents
    ]
}

# TOC depth for the local table of contents
toc_object_entries_show_parents = "hide"  # Cleaner display of nested items
