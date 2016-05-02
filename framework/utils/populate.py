"""Persistent data fixtures.

TODO:
+   Async-like architecture.
+   Keep old data; quit dropping *everything*.
"""

from .. import extensions, models
from ..extensions import fixtures
from .imports import all_models

from ..models.attribute import Attribute
from ..models.element import Element
from ..models.route import Route
from ..models.setting import Setting
from ..models.site import Site
from ..models.template import Template


'''
    populate: performs build commands
    build:    provides structures
'''

displays = 2
display_num = range(displays)  # Unresponsive > 3


def populate_all():
    """Initalize the async worker."""

    #e()

    #return None

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

    # 26-total items
    d = {
        1: [( 1,None,'head'),
            ( 4,None,'body')
           ],
        2: [( 2, 1, 'title'),
            ( 3, 1, 'meta'),
            ( 5, 4, 'navbar'),
            (20, 4, 'content'),
            (23, 4, 'footer')
           ],
        3: [( 6, 5, 'nav_head'),
            ( 7, 5, 'nav'),
            (14, 5, 'nav_right'),
            (21,20, 'h1'),
            (22,20, 'div'),
            (24,23, 'ul'),
            (27,23, 'p')
           ],
        4: [( 8, 7, 'brand'),
            ( 9, 7, 'links'),
            (13, 7, 'thing'),
            (15,14, 'a'),
            (16,14, 'ul'),
            (19,14, 'a'),
            (25,24, 'li'),
            (26,24, 'li')
           ],
        5: [(10, 9, 'ul'),
            (17,16, 'li'),
            (18,16, 'li')
           ],
        6: [(11,10, 'li'),
            (12,10, 'li')
           ]
    }

    k = {}
    for level in d:
        for o in d[level]:
            k[o[0]] = None

    fin_rows = 0
    fin_templates = 0
    while True:
        tid = templates[fin_templates].id

        for level in d:
            elements = d[level]
            order = 1

            for element in elements:
                if level == 1: # top-row
                    e = fixtures.blend(Element, tag=element[2], order=fin_templates, template=tid)
                else:
                    e = fixtures.blend(Element, tag=element[2], order=order, template=tid, parent=k[element[1]].id)
                k[element[0]] = e
                order += 1

        # Break
        fin_rows += 1
        if fin_rows == displays:
            fin_templates += 1
            fin_rows = 0
        if fin_templates == templates.__len__():
            break
