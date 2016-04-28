"""Foundation for multi-site."""

from ..extensions import db
from .setting import Setting


class Site(db.Model):
    """TODO."""

    __tablename__ = 'sites'

    id = db.Column(db.Integer, primary_key=True)

    def settings_as_dict(self):
        """TODO."""

        query = Setting.query.filter_by(site_id=self.id).all()
        struct = {}
        for setting in query:
            struct[setting.key] = setting.value
        return struct

    def setting_value(self, key):
        """TODO."""

        return Setting.query. \
            filter_by(site_id=self.id). \
            filter_by(key=key). \
            first(). \
            value

    @property
    def href(self):
        """TODO."""

        return '<a href="/{site_id}">{site_title}</a>'.format(
            site_id=self.id,
            site_title=self.setting_value('Title')
        )
