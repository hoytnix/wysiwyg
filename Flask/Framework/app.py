#!/usr/bin/env python

"""
app
~~~

MV(C).

:copyright: (c) 2016 Michael Hoyt. <@pr0xmeh>
:license: Anavah.
"""

from flask import Flask

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from .blueprint import blueprints
from .config import Config
from .extensions import db

from .utils.fs import abs_fs
from .utils.imports import all_models

def create_app():
    config = Config()

    # Initialize the app object.
    app = Flask(import_name=__name__, template_folder=abs_fs['templates'])

    # Attempt to configure from python-object.
    app.config.from_object(config)

    configure_blueprints(app)
    configure_extensions(app)

    return app

def configure_blueprints(app):
    app.register_blueprint(blueprints, url_prefix='')

def configure_extensions(app):
    # flask_sqlalchemy
    with app.app_context():
        db.init_app(app)

    # flask_admin
    admin = Admin(app, url='/admin', name='Anavah', template_mode='bootstrap3')
    for model in all_models():
        admin.add_view(ModelView(model, db.session))

