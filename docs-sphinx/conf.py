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

# Sphinx Book Theme - left sidebar TOC similar to TypeDoc
html_theme = "sphinx_book_theme"
html_theme_options = {
    "show_toc_level": 3,  # Show 3 levels deep in left sidebar TOC
    "navigation_with_keys": True,
}

# Cleaner display - remove module prefixes from class/function names
add_module_names = False

# Cleaner display of nested items in TOC
toc_object_entries_show_parents = "hide"

# Move type hints from signatures to description section
autodoc_typehints = "description"

# Simplify signature display
autodoc_typehints_format = "short"
