# -*- coding: utf-8 -*-

import os
from flask import Flask
from dpage import views


def create_app(debug=True):
    print(__name__)
    _app = Flask(__name__, template_folder='dpage/templates', static_folder='dpage/static')
    _app.debug = debug
    _app.config.from_object('settings')
    if 'FLASK_CONF' in os.environ:
        app.config.from_envvar('FLASK_CONF')

    views.init(_app)
    return _app

app = create_app()