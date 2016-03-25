"""Persistent data fixtures.

TODO:
+   Async-like architecture.
+   Keep old data; quit dropping *everything*.
"""

from .. import extensions, models
from ..extensions import fixtures
from ..models import Site, Setting, Route, Template, Element, Attribute
from .imports import all_models

'''
    populate: performs build commands
    build:    provides structures
'''

display_num = range(2)  # Unresponsive > 3


def populate_all():
    """Initalize the async worker."""

    for iteration in display_num:
        site = fixtures.blend(Site)
        populate_settings(site)
        routes = populate_routes(site)
        templates = populate_templates(routes)
        elements = populate_elements(templates)


def populate_settings(site):
    """Initialize Settings."""

    fixture_data = [
        ('Title', 'Anavah {}'.format(site.id)),
        ('Theme', 'superhero')
    ]

    for item in fixture_data:
        fixtures.blend(Setting, site_id=site.id, key=item[0], value=item[1])


def populate_routes(site):
    """Initialize Routes."""

    routes = []
    for iteration in display_num:
        _r = fixtures.blend(Route, path=str(iteration), parent=site.id)
        routes.append(_r)
    return routes


def populate_templates(routes):
    """Initialize Templates."""

    templates = []
    iteration = 0
    for route in routes:
        _t = fixtures.blend(Template, file=str(iteration), parent=route.id)
        templates.append(_t)
        iteration += 1
    return templates


def populate_elements(templates):
    """Initialize Elements."""

    elements = []
    iteration = 0
    for template in templates:
        for iteration in display_num:
            tid = template.id

            top_nav = fixtures.blend(Element, tag='top_nav', order=iteration, template=tid)

            container = fixtures.blend(Element, tag='container', order=1, template=tid, parent=top_nav.id)

            navbar_header = fixtures.blend(Element, tag='navbar_header', order=1, template=tid, parent=top_nav.id)
            navbar = fixtures.blend(Element, tag='navbar', order=2, template=tid, parent=top_nav.id)
            navbar_footer = fixtures.blend(Element, tag='navbar_footer', order=3, template=tid, parent=top_nav.id)

            nav = fixtures.blend(Element, tag='nav', order=1, template=tid, parent=navbar.id)
            nav_right = fixtures.blend(Element, tag='nav_right', order=2, template=tid, parent=navbar.id)
