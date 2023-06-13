# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# #project-information

import os
import sys

sys.path.insert(0, os.path.abspath('../..'))

project = 'Ask YouTube Playlists'
copyright = '2023, Pablo Ariño, Beatriz Correia, Álvaro Laguna'
author = 'Pablo Ariño, Beatriz Correia, Álvaro Laguna'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# #general-configuration

extensions = ['sphinx.ext.napoleon',
              'sphinx.ext.autodoc',
              'sphinx.ext.viewcode',
              'hoverxref.extension',
              'sphinx_last_updated_by_git']

templates_path = ['_templates']
exclude_patterns = []
pygments_style = 'colorful'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# #options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ['style.css']
html_context = {
    "default_mode": "auto"
}
