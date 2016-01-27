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

from blueprint import blueprints
from config import Config
from extensions import db

from utils.imports import all_models

def create_app():
    config = Config()

    app = Flask(import_name=__name__, template_folder='./templates')
    app.config.from_object(config)
    app.register_blueprint(blueprints, url_prefix='')

    configure_admin(app)
    configure_extensions(app)

    return app

def configure_admin(app):
    admin = Admin(app, url='/admin', name='Anavah', template_mode='bootstrap3')
    for model in all_models():
        admin.add_view(ModelView(model, db.session))

def configure_extensions(app):
    # flask_sqlalchemy
    db.init_app(app)


