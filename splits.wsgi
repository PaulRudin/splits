# -*- mode: python; -*-

# enable mod_wsgi and mount this with e.g. WSGIScriptAlias /splits
# /path/to/here/splits.wsgi in your apache configuration
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from webapp import app as application
