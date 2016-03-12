"""The (M)odel in (M)VC."""

from flask import current_app
from random import choice
import copy
import pprint

from . import extensions
from .extensions import db


class Site(db.Model):
    """TODO."""

    __tablename__ = 'sites'

    id = db.Column(db.Integer, primary_key=True)

    def settings_as_dict(self):
        """TODO."""

        query = Setting.query.filter_by(site_id=self.id).all()
        struct = {}
        for setting in query:
            struct[setting.key] = setting.value
        return struct

    def setting_value(self, key):
        """TODO."""

        return Setting.query. \
            filter_by(site_id=self.id). \
            filter_by(key=key). \
            first(). \
            value

    @property
    def href(self):
        """TODO."""

        return '<a href="/{site_id}">{site_title}</a>'.format(
            site_id=self.id,
            site_title=self.setting_value('Title')
        )


class Setting(db.Model):
    """TODO."""

    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, nullable=False)
    key = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(255), nullable=False)

    @property
    def name(self):
        """TODO."""

        return self.key


class Route(db.Model):
    """TODO."""

    __tablename__ = 'routes'

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255), nullable=False)
    parent = db.Column(db.Integer, nullable=False)

    @property
    def child(self):
        """TODO."""

        return Template.query.filter_by(parent=self.id).first()


class Template(db.Model):
    """TODO."""

    __tablename__ = 'templates'

    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(255), nullable=False)
    parent = db.Column(db.Integer, nullable=False)

    @property
    def element_dict(self):
        """TODO."""

        store = {}
        d = {
            'self': None,
            'children': {}
        }
        level = 0

        # 'Rows': Highest-level in order-heirarchy, where parent = None
        rows = Element.query. \
            filter_by(template=self.id, parent=None). \
            order_by(Element.order).all()
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
        """TODO."""

        return Route.query.get(self.parent)


class Element(db.Model):
    """TODO."""

    __tablename__ = 'elements'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(255), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    template = db.Column(db.Integer, nullable=False)
    parent = db.Column(db.Integer, nullable=True)

    @property
    def children(self):
        """TODO."""

        return Element.query.filter_by(parent=self.id).all()

    @property
    def attribute_dict(self):
        """TODO."""

        d = {}
        attributes = Attribute.query.filter_by(parent=self.id).all()
        for attribute in attributes:
            d[attribute.key] = attribute.value
        return d


class Attribute(db.Model):
    """TODO."""

    __tablename__ = 'attributes'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(255), nullable=False)
    parent = db.Column(db.Integer, nullable=False)
