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
import copy
import pprint


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
            site_id=self.id,
            site_title=self.setting_value('Title')
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
    parent = db.Column(db.Integer, nullable=False)

    @property
    def child(self):
        return SiteTemplate.query.filter_by(parent=self.id).first()

    def __init__(self, path, parent):
        self.path = path
        self.parent = parent

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


class SiteTemplate(db.Model):
    __tablename__ = 'site_templates'

    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(255), nullable=False)
    parent = db.Column(db.Integer, nullable=False)

    @property
    def element_dict(self):
        store = {}
        d = {
            'self': None,
            'children': {}
        }
        level = 0

        # 'Rows': Highest-level in order-heirarchy, where parent = None
        rows = TemplateElement.query. \
            filter_by(template=self.id, parent=None). \
            order_by(TemplateElement.order).all()
        row_n = 0
        for row in rows:
            row_n += 1
            row_key = 'row_{}'.format(row_n)

            row_s = copy.deepcopy(d)
            row_s['self'] = row

            store[row_key] = row_s

        # After that, elements may have an infinite nesting of children.
        pointer = store
        while True:
            keys = [key for key in pointer.keys()]

            for key in keys:
                return None
            children = row['self'].children
            if children:
                for child in children:
                    k = str(child.order)
                    row['children'][k] = copy.deepcopy(d)
            else:
                break
            break
            '''
                # 2. Add it to the latest heirarchy level...
                element = row['todo'][0]
                k = str(element.order)
                row['children'][k] = copy.deepcopy(d)
                row['children'][k]['self'] = copy.deepcopy(element)
                # 3. Move the item from todo to done.
                row['todo'].remove(element)
                # . Populate new queue.
                row['children'][k]['todo'] = element.children
                #
                #row = row['children']
            # 4. If empty queue, check for a new level.
            '''
        store[row_key] = row

        # Verbosity, thank you.
        pprint.pprint(store, indent=4, width=120)

    @property
    def owner(self):
        return SiteRoute.query.get(self.parent)

    def __init__(self, file, parent):
        self.file = file
        self.parent = parent

        db.session.add(self)
        db.session.commit()


class TemplateElement(db.Model):
    __tablename__ = 'template_elements'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(255), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    template = db.Column(db.Integer, nullable=False)
    parent = db.Column(db.Integer, nullable=True)

    @property
    def children(self):
        return TemplateElement.query.filter_by(parent=self.id).all()

    @property
    def attribute_dict(self):
        d = {}
        attributes = ElementAttribute.query.filter_by(parent=self.id).all()
        for attribute in attributes:
            d[attribute.key] = attribute.value
        return d

    def __init__(self, template, tag, order, parent=None):
        self.template = template
        self.tag = tag
        self.order = order

        if parent:
            self.parent = parent

        db.session.add(self)
        db.session.commit()


class ElementAttribute(db.Model):
    __tablename__ = 'element_attributes'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(255), nullable=False)
    parent = db.Column(db.Integer, nullable=False)

    def __init__(self, key, value, parent):
        self.key = key
        self.value = value
        self.parent = parent

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
