#!/usr/bin/env python

"""
config
~~~~~~~~~~~~~~~~~~~~~~~

Flask config object.

:copyright: (c) 2016 Michael Hoyt. <@pr0xmeh>
:license: Anavah.
"""

class Config:
    def __init__(self):
        # SQLAlchemy
        self.SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(
            'anavah',
            'seal-hello-boat',
            'anavah-dev.celgo7igyrro.us-east-1.rds.amazonaws.com',
            'anavah'
        )
        self.SQLALCHEMY_ECHO = False
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False

        # Security
        self.SECRET_KEY = 'secret'
        self.WTF_CSRF_ENABLED = True
        self.WTF_CSRF_SECRET_KEY = 'secret'

        # General
        self.DEBUG = True


