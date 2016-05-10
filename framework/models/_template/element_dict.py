"""An element_dict is a level-order structure to represent HTML.

+ Ultimately can be reverse-engineered to a string-representation of HTML.
+ Level-order provides hierarchy and inheritance, two important concepts to DOM.

They look a little like this:

1: (-, (
    2: (-, {
            3: (-, None),
            4: (-, {
                    5: (-, None),
                    6: (-, None)
                    },
            ),
            7: (-, None)
            }
        )
    )
)

NOTE: \-\ = self
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
        queue[top_key][0] = []  # Level-0
        queue[top_key][0].append(top_element)

        # 2. Recursively add children to next level.
        new_level = 1
        while True:
            do_continue = False
            first = True

            queue_prev_level = queue[top_key][(new_level-1)]
            queue_curr_level = None
            for parent in queue_prev_level:
                children = parent.children

                if children.__len__() > 0:
                    do_continue = True  # If any in level have children.
                    if first:
                        queue[top_key][(new_level)] = []
                        queue_curr_level = queue[top_key][(new_level)]
                        first = False

                    for child in children:
                        queue_curr_level.append(child)

            if not do_continue:  # None have children
                break
            else:
                new_level += 1

    # Debug verbosity.
    debug_print(queue, title='INITIAL QUEUE')


    e_dict = Tree()  # returnable
    pointer = []  # [n-parent, parent, child, child-n, ...]

    for row_key in queue:
        '''Indexes: e_dict[row_key]'''

        pointer = []  # reset

        # Add the top-level.
        row = queue[row_key]
        top_element = row[0][0]
        pointer.append(top_element)
        e_dict.add(pointer)

        # debug_step = 100
        # steps = 0
        queue_level = 1
        while True:
            steps += 1

            if queue[row_key][1].__len__() == 0:
                queue[row_key][0] = []

            if queue[row_key][0].__len__() == 0:
                steps = 0
                queue_level = 0
                break

            parent = pointer[-1]
            parent_queue = queue[row_key][queue_level - 1]

            if queue_level not in queue[row_key]:
                # print('{}: Inexistent level'.format(queue_level))

                # if steps == debug_step:
                #     print(parent)
                #     print(parent_queue)
                #     #return None

                queue_level -= 1
                parent_queue.remove(parent)
                pointer = pointer[:-1]
                continue

            # TODO: Won't work for a row with no children.
            child_queue  = queue[row_key][queue_level]

            # Relationship comparison
            found_children = False
            for child in child_queue:
                if child in parent.children:
                    # print('{}: Found a child'.format(queue_level))

                    # if steps == debug_step:
                    #     print(parent)
                    #     print(parent_queue)
                    #     #return None

                    found_children = True
                    pointer.append(child)
                    e_dict.add(pointer)

                    queue_level += 1

                    break  # Only perform for one element per loop.

            if not found_children:
                # print('{}: No children found'.format(queue_level))

                # if steps == debug_step:
                #     print(parent)
                #     print(parent_queue)
                #     #return None

                queue_level -= 1
                parent_queue.remove(parent)
                pointer = pointer[:-1]

            # if steps == debug_step:
            #     steps = 0
            #     queue_level = 0
            #     break


    # Verbosity, thank you.
    # e_dict.print()

    return e_dict
