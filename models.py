#!/usr/bin/env python

"""
models
~~~~~~

(M)VC.

:copyright: (c) 2016 Michael Hoyt. <@pr0xmeh>
:license: Anavah.
"""

from extensions import db

from random import choice


'''
    Database models.
'''

class Test(db.Model):
    __tablename__ = 'test'

    key = db.Column(db.String(255), primary_key=True)
    value = db.Column(db.String(255), nullable=False)

    @property
    def name(self):
        return self.value




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

