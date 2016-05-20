from ..extensions import db


class Site(db.Model):
    """Abstract class to provide inheritance."""

    __tablename__ = 'sites'

    id = db.Column(db.Integer, primary_key=True)

    def settings_as_dict(self):
        query = Setting.query.filter_by(site_id=self.id).all()
        struct = {}
        for setting in query:
            struct[setting.key] = setting.value
        return struct

    def setting_value(self, key):
        return Setting.query. \
            filter_by(site_id=self.id). \
            filter_by(key=key). \
            first(). \
            value

    @property
    def href(self):
        return '<a href="/{site_id}">{site_title}</a>'.format(
            site_id=self.id,
            site_title=self.setting_value('Title')
        )

class Setting(db.Model):
    """Key-value of a site-property."""

    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, nullable=False)
    key = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(255), nullable=False)

    @property
    def name(self):
        return self.key
