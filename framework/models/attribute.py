"""Key-value of HTML-property.

Example:
<p class="new">...
`class` is the key, and `new` is the value.
"""

from ..extensions import db


class Attribute(db.Model):
    __tablename__ = 'attributes'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(255), nullable=False)
    parent = db.Column(db.Integer, nullable=False)
