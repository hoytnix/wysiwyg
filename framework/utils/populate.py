"""Persistent data fixtures.

TODO:
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


displays = 2
display_num = range(displays)  # Unresponsive > 3


def populate_all():
    """Perform all table populations."""

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
    # level: (id, parent, order, tag)
    struct = {
        1: [( 1,None,1,'head'),
            ( 4,None,2,'body'),
            (99,None,3,'childless')
           ],
        2: [( 2, 1, 1, 'title'),
            ( 3, 1, 2, 'meta'),

            ( 5, 4, 1, 'navbar'),
            (20, 4, 2, 'content'),
            (23, 4, 3, 'footer')
           ],
        3: [( 6, 5, 1, 'nav_head'),
            ( 7, 5, 2, 'nav'),
            (14, 5, 3, 'nav_right'),

            (21,20, 1, 'h1'),
            (22,20, 2, 'div'),

            (24,23, 1, 'ul'),
            (27,23, 2, 'p')
           ],
        4: [( 8, 7, 1, 'brand'),
            ( 9, 7, 2, 'links'),
            (13, 7, 3, 'thing'),

            (15,14, 1, 'a'),
            (16,14, 2, 'ul'),
            (19,14, 3, 'a'),

            (25,24, 1, 'li'),
            (26,24, 2, 'li')
           ],
        5: [(10, 9, 1, 'ul'),

            (17,16, 1, 'li'),
            (18,16, 2, 'li')
           ],
        6: [(11,10, 1, 'li'),
            (12,10, 2, 'li')
           ]
    }

    store = {}
    for level in struct:
        for obj in struct[level]:
            store[obj[0]] = None

    for template in templates:
        for level in struct:
            elements = struct[level]

            for element in elements:
                _id = element[0]
                parent = element[1]
                v = {
                    'template': template.id,
                    'order': element[2],
                    'tag': element[3]
                }
                if parent:
                    v['parent'] = store[parent].id

                new_element = fixtures.blend(Element, **v)
                store[_id] = new_element
