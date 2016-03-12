"""Extensions for Flask."""

from flask_admin import Admin
from flask.ext.sqlalchemy import SQLAlchemy
from mixer.backend.flask import mixer


admin = Admin

db = SQLAlchemy()

fixtures = mixer
