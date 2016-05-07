"""Highest-level interface for interacting with templates.

Templates should:
+ Be modular; small-changes will not require re-compiling EVERYTHING.
+ Never be more to the public than their string-representations:
    + All the work will be handled on the backend (here).
    + Strings can be serialized by ANYTHING!
"""

from ..extensions import db
from ._template.element_dict import template_to_element_dict


class Template(db.Model):
    __tablename__ = 'templates'

    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(255), nullable=False)
    parent = db.Column(db.Integer, nullable=False)

    @property
    def element_dict(self):
        return template_to_element_dict(template=self)

    @property
    def owner(self):
        return Route.query.get(self.parent)
