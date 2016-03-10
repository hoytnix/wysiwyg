"""The (M)odel in (M)VC."""

from flask import current_app

from .extensions import db

from random import choice
import copy
import pprint


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

    def __init__(self):
        """TODO."""

        db.session.add(self)
        db.session.commit()


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

    def __init__(self, path, parent):
        """TODO."""

        self.path = path
        self.parent = parent

        db.session.add(self)
        db.session.commit()


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

    def __init__(self, site_id, key, value):
        """TODO."""

        self.site_id = site_id
        self.key = key
        self.value = value

        db.session.add(self)
        db.session.commit()


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
        """TODO."""

        return Route.query.get(self.parent)

    def __init__(self, file, parent):
        """TODO."""

        self.file = file
        self.parent = parent

        db.session.add(self)
        db.session.commit()


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

    def __init__(self, template, tag, order, parent=None):
        """TODO."""

        self.template = template
        self.tag = tag
        self.order = order

        if parent:
            self.parent = parent

        db.session.add(self)
        db.session.commit()


class Attribute(db.Model):
    """TODO."""

    __tablename__ = 'attributes'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(255), nullable=False)
    parent = db.Column(db.Integer, nullable=False)

    def __init__(self, key, value, parent):
        """TODO."""

        self.key = key
        self.value = value
        self.parent = parent

        db.session.add(self)
        db.session.commit()


'''
    Randomized data models.
'''


def bootstrap_template():
    """TODO."""

    return choice([
        'cerulean', 'cosmo', 'cyborg', 'darkly', 'flatly', 'journal', 'lumen',
        'paper', 'readable', 'sandstone', 'simplex', 'slate', 'spacelab',
        'superhero', 'united', 'yeti'
    ])
