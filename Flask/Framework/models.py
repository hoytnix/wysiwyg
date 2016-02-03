#!/usr/bin/env python

"""
models
~~~~~~

(M)VC.

:copyright: (c) 2016 Michael Hoyt. <@pr0xmeh>
:license: Anavah.
"""

from flask import current_app

from .extensions import db

from random import choice


'''
    Database models.
'''

class Site(db.Model):
    __tablename__ = 'sites'

    id = db.Column(db.Integer, primary_key=True)

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

    def __init__(self):
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

bootstrap_template = choice([
    'cerulean', 'cosmo', 'cyborg', 'darkly', 'flatly', 'journal', 'lumen',
    'paper', 'readable', 'sandstone', 'simplex', 'slate', 'spacelab',
    'superhero', 'united', 'yeti'
])

user = choice([
    {
        'name': 'Oloty'
    }
])

