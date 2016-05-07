"""Key-value of a site-property."""

from ..extensions import db


class Setting(db.Model):
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, nullable=False)
    key = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(255), nullable=False)

    @property
    def name(self):
        return self.key
