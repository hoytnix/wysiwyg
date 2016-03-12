"""The (C)ontroller in MV(C)."""

from flask import Flask

from flask_admin.contrib.sqla import ModelView

from . import blueprint, config, extensions
from .blueprint import blueprints
from .config import Config
from .extensions import admin, db, fixtures

from .utils.fs import abs_fs
from .utils.imports import all_models


def create_app():
    """Create an application factory.

    http://flask.pocoo.org/docs/0.10/patterns/appfactories/
    """

    # Initialize the app object.
    app = Flask(import_name=__name__, template_folder=abs_fs['templates'])

    # Attempt to configure from python-object.
    app.config.from_object(config.Config())

    configure_blueprints(app)
    configure_extensions(app)

    return app


def configure_blueprints(app):
    """Register the application blueprints.

    TODO: Iterate through an index.
    """

    app.register_blueprint(blueprint.blueprints, url_prefix='')


def configure_extensions(app):
    """Register Flask's extensions."""

    # flask_sqlalchemy
    with app.app_context():
        db.init_app(app)

    # mixture
    with app.app_context():
        fixtures.init_app(app)

    # flask_admin
    _admin = admin(app, url='/admin', name='Anavah', template_mode='bootstrap3')
    for model in all_models():
        _admin.add_view(ModelView(model, db.session))
