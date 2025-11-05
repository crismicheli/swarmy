# conf.py -- Swarmy Documentation

import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

project = 'Swarmy'
author = 'your name'
release = '1.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',
    'sphinx.ext.githubpages',
    'sphinx.ext.mathjax',
]

autosummary_generate = True
napoleon_google_docstring = True
napoleon_numpy_docstring = True

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'
