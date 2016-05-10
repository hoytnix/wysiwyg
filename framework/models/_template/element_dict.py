"""An element_dict is a level-order structure to represent HTML.

+ Ultimately can be reverse-engineered to a string-representation of HTML.
+ Level-order provides hierarchy and inheritance, two important concepts to DOM.

They look a little like this:

{'element_dict': {'element_dict': {},
                  (1, <head>): {(1, <title>): {}, (2, <meta>): {}},
                  (2, <body>): {(1, <navbar>): {(1, <nav_head>): {},
                                                (2, <nav>): {(1, <brand>): {},
                                                             (2, <links>): {(1, <ul>): {(1, <li>): {},
                                                                                        (2, <li>): {}}},
                                                             (3, <thing>): {}},
                                                (3, <nav_right>): {(1, <a>): {},
                                                                   (2, <ul>): {(1, <li>): {},
                                                                               (2, <li>): {}},
                                                                   (3, <a>): {}}},
                                (2, <content>): {(1, <h1>): {}, (2, <div>): {}},
                                (3, <footer>): {(1, <ul>): {(1, <li>): {},
                                                            (2, <li>): {}},
                                                (2, <p>): {}}},
                  (3, <childless>): {}}}
"""

from ..element import Element

from ...utils.helpers import debug_print

from collections import defaultdict
from pprint import pprint


class Tree:
    """https://gist.github.com/hrldcpr/2012250"""

    def __init__(self):
        self.store = self.tree_struct()
        self.add(['element_dict'])

    def add(self, keys):
        _keys = ['element_dict']
        for key in keys:
            _keys.append(key)

        t = self.store
        for key in _keys:
            t = t[key]

    def print(self):
        d = self.dicts(self.store)
        pprint(d, indent=4, width=80)

    def dicts(self, t):
        return {k: self.dicts(t[k]) for k in t}

    def tree_struct(self):
        return defaultdict(self.tree_struct)


def template_to_element_dict(template):
    # Elemnts at the highest-level. Specialized because parent=None.
    top_elements = []
    top_query = Element.query. \
        filter_by(template=template.id, parent=None). \
        order_by(Element.order).all()

    for top_element in top_query:
        top_elements.append(top_element)

    # Level queue.
    queue = {}
    for top_element in top_elements:
        # 1. Populate highest-level with the element itself.
        top_key = top_element.order
        queue[top_key] = {}
        queue_cursor = queue[top_key]
        queue_cursor[0] = top_element

        # 2. Top-element already has a `children` function:
        top_children = top_element.children
        if top_children.__len__() > 0:
            queue_cursor[1] = top_children
        else:
            break  # No reason to continue.

        # 3. Recursively add children to next level.
        new_level = 2
        while True:
            has_children = False
            first = True

            queue_parent = queue_cursor[(new_level - 1)]
            queue_child = None
            for parent in queue_parent:
                children = parent.children

                if children.__len__() > 0:
                    has_children = True

                    if first:
                        queue_cursor[new_level] = []
                        queue_child = queue_cursor[new_level]
                        first = False

                    for child in children:
                        queue_child.append(child)

            if not has_children:
                break
            else:
                new_level += 1

    e_dict = Tree()  # returnable
    pointer = []  # [n-parent, parent, child, child-n, ...]

    for row_key in queue:
        pointer = []  # reset
        queue_row = queue[row_key]

        # Add the top-level.
        top_element = queue_row[0]
        top_element_key = (top_element.order, top_element)
        pointer.append(top_element_key)
        e_dict.add(pointer)

        queue_level = 1
        while True:
            if 1 not in queue_row:
                break  # No reason to continue.

            if queue_row[1].__len__() == 0:
                break

            parent = pointer[-1][1]
            parent_queue = queue_row[queue_level - 1]

            if queue_level not in queue_row:
                queue_level -= 1
                parent_queue.remove(parent)
                pointer = pointer[:-1]
                continue

            # Reserved until after a level-check to avoid unnecessary action.
            parent_children = parent.children
            child_queue = queue_row[queue_level]

            found_children = False
            for child in child_queue:
                if child in parent_children:
                    found_children = True
                    queue_level += 1
                    child_key = (child.order, child)
                    pointer.append(child_key)
                    e_dict.add(pointer)

                    break  # Only perform for one element per loop.

            if not found_children:
                queue_level -= 1
                parent_queue.remove(parent)
                pointer = pointer[:-1]

    return e_dict
