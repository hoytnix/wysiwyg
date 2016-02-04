#!/usr/bin/env python

"""
anavah.utils.populate
~~~~~~~~~~~~~~~~~~~~~

Persistent data for development.

:copyright: (c) 2016 Michael Hoyt. <@pr0xmeh>
:license: Anavah.
"""

from ..models import Site, SiteSetting
from ..models import bootstrap_template

'''
    populate: performs build commands
    build:    provides structures
'''

def populate_all():
    populate_sites()
    populate_site_settings()

def populate_sites():
    build_sites()

def populate_site_settings():
    build_site_settings()

def build_sites():
    for i in range(10):
        Site()

def build_site_settings():
    sites = Site.query.all()
    for site in sites:
        fixture_data = [
            ('Title', 'Anavah {}'.format(site.id)),
            ('Theme', bootstrap_template()),
            ('Hash', site.id_hash)
        ]
        for fixture_group in fixture_data:
            SiteSetting(site_id = site.id, key=fixture_group[0], value=fixture_group[1])
