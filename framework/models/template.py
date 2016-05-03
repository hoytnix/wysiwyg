"""High-level template logic."""

from ..extensions import db
from ._template.element_dict import template_to_element_dict


class Template(db.Model):
    """TODO."""

    __tablename__ = 'templates'

    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(255), nullable=False)
    parent = db.Column(db.Integer, nullable=False)

    @property
    def element_dict(self):
        """TODO."""

        return template_to_element_dict(template=self)

    @property
    def owner(self):
        """TODO."""

        return Route.query.get(self.parent)
