#!/usr/bin/env python

"""
app
~~~

MV(C).

:copyright: (c) 2016 Michael Hoyt. <@pr0xmeh>
:license: Anavah.
"""

from flask import Flask

from blueprint import blueprints
from config import Config


def create_app():
    config = Config()

    app = Flask(import_name=__name__, template_folder='./templates')
    app.config.from_object(config)
    app.register_blueprint(blueprints, url_prefix='')

    return app
