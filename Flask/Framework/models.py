#!/usr/bin/env python

"""
anavah.models
~~~~~~~~~~~~~

(M)VC.

:copyright: (c) 2016 Michael Hoyt. <@pr0xmeh>
:license: Anavah.
"""

from flask import current_app

from .extensions import db
from .utils.helpers import md5_hash

from random import choice


'''
    Database models.
'''

class Site(db.Model):
    __tablename__ = 'sites'

    id = db.Column(db.Integer, primary_key=True)

    def settings_as_dict(self):
        query = SiteSetting.query.filter_by(site_id=self.id).all()
        struct = {}
        for setting in query:
            struct[setting.key] = setting.value
        return struct

    def setting_value(self, key):
        return SiteSetting.query. \
            filter_by(site_id=self.id). \
            filter_by(key=key). \
            first(). \
            value

    @property
    def href(self):
        return '<a href="/{site_id}">{site_title}</a>'.format(
            site_id = self.id,
            site_title = self.setting_value('Title')
        )

    @property
    def id_hash(self):
        return md5_hash(self.id)

    def __init__(self):
        db.session.add(self)
        db.session.commit()


class SiteRoute(db.Model):
    __tablename__ = 'site_routes'

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255), nullable=False)

    def __init__(self, path):
        self.path = path

        db.session.add(self)
        db.session.commit()


class SiteSetting(db.Model):
    __tablename__ = 'site_settings'

    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, nullable=False)
    key = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(255), nullable=False)

    @property
    def name(self):
        return self.key

    def __init__(self, site_id, key, value):
        self.site_id = site_id
        self.key = key
        self.value = value

        db.session.add(self)
        db.session.commit()

'''
    Randomized data models.
'''

def bootstrap_template():
    return choice([
    'cerulean', 'cosmo', 'cyborg', 'darkly', 'flatly', 'journal', 'lumen',
    'paper', 'readable', 'sandstone', 'simplex', 'slate', 'spacelab',
    'superhero', 'united', 'yeti'
    ])

