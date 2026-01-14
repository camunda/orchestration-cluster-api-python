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
