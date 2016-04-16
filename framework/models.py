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

        store = []

        # 'Rows': Highest-level in order-heirarchy, where parent = None
        rows = Element.query. \
            filter_by(template=self.id, parent=None). \
            order_by(Element.order).all()
        row_n = 0
        for row in rows:
            store.append((row_n, row, []))
            row_n += 1

        # Create a level queue.
        queue = {}
        row_keys = [x[0] for x in store]
        for row_key in row_keys:
            # 1. Populate highest-level with the row itself.
            queue[row_key] = {}
            queue[row_key]['0'] = []
            for k in store:
                if k[0] == row_key:
                    queue[row_key]['0'].append(k[1])

            # 2. Recursively add children to next level.
            new_level = 1
            while True:
                do_continue = False
                first = True
                for parent in queue[row_key][str(new_level - 1)]:
                    children = parent.children
                    if children.__len__() > 0:
                        do_continue = True
                        if first:
                            queue[row_key][str(new_level)] = []
                            first = False
                        for child in children:
                            queue[row_key][str(new_level)].append(child)
                if not do_continue:  # None have children
                    break
                else:
                    new_level += 1

        '''
        1) Add top-level (0).
        2) Recursive:
            a) for element in row:
            b)   for _element in row+1:
            c)     if _element in element.children:
            d)       win.
        '''

        # pprint.pprint(queue, indent=4, width=80)
        # return None

        row_keys = [x[0] for x in store]
        for row in row_keys:
            level = 0
            while True:
                curr_key = str(level)
                next_key = str(level + 1)

                if next_key not in queue[row]:
                    break  # No more levels!

                for e in queue[row][curr_key]:
                    for _e in queue[row][next_key]:
                        if _e in e.children:
                            print(new_level, _e.order, e.tag, _e.tag)
                level += 1

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
