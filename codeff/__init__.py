import os, os.path as op; __dir__ = op.dirname(op.abspath(__file__))
from flask import Flask


app = Flask(__name__, static_folder=op.join(op.dirname(__dir__), 'static'))

# JINJA ------------------------------------------------------------------------
app.jinja_env.globals['locale'] = lambda: 'en'

# VIEWS ------------------------------------------------------------------------
import codeff.views
