#!/usr/bin/env python

"""
anavah.utils.populate
~~~~~~~~~~~~~~~~~~~~~

Persistent data for development.

:copyright: (c) 2016 Michael Hoyt. <@pr0xmeh>
:license: Anavah.
"""

from ..models import Site, SiteSetting, SiteRoute, SiteTemplate, TemplateElement, ElementAttribute
from ..models import bootstrap_template
from .imports import all_models

'''
    populate: performs build commands
    build:    provides structures
'''

display_num = 2  # Unresponsive > 3; Elements complexity as of 02-12-16


def populate_all():
    print('Populating sites...')
    build_sites()

    print('Populating site settings...')
    build_site_settings()

    print('Populating site routes...')
    build_routes()

    print('Populating templates...')
    build_templates()

    print('Populating template elements...')
    build_template_elements()


def build_sites():
    for i in range(display_num):
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
            SiteSetting(site_id=site.id, key=fixture_group[0], value=fixture_group[1])


def build_routes():
    sites = Site.query.all()
    for site in sites:
        for i in range(display_num):
            SiteRoute(parent=site.id, path=str(i))


def build_templates():
    routes = SiteRoute.query.all()
    for route in routes:
        file = '{}.html'.format(route.id)
        parent = route.id
        SiteTemplate(file=file, parent=parent)


def build_template_elements():
    templates = SiteTemplate.query.all()
    for template in templates:
        for iteration in range(display_num):
            top_nav = TemplateElement(tag='top_nav', order=iteration + 1, template=template.id)

            container = TemplateElement(tag='container', order=1, template=template.id, parent=top_nav.id)

            navbar_header = TemplateElement(tag='navbar_header', order=1, template=template.id, parent=container.id)
            navbar = TemplateElement(tag='navbar', order=2, template=template.id, parent=container.id)
            navbar_footer = TemplateElement(tag='navbar_footer', order=3, template=template.id, parent=container.id)

            nav = TemplateElement(tag='nav', order=1, template=template.id, parent=navbar.id)
            nav_right = TemplateElement(tag='nav_right', order=2, template=template.id, parent=navbar.id)
