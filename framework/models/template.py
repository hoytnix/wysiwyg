"""High-level template logic."""

from ..extensions import db
from ..utils.helpers import debug_print
from .element import Element


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
        '''

        # Debug verbosity.
        # debug_print(title='QUEUE', data=queue)

        e_dict = {}
        row_keys = [x[0] for x in store]

        for row in row_keys:
            # First
            e_dict[row] = {}

            # Convenience pointers
            r_cur = e_dict[row]
            q_cur = queue[row]

            # Populate first for operation.
            for e_cur in q_cur["0"]:
                # print(e_cur.tag, e_cur.order)
                r_cur[e_cur.order] = [e_cur, None]

            # Loop for each top-level element.
            te_keys = [x for x in r_cur]

            for te_key in te_keys:
                # Top-element pointer
                te_cur = r_cur[te_key]

                # Tree-level counter
                level = 1

                steps = 1
                # Tree traversal
                grandparent_pointer = [None]
                parent_pointer = [te_cur]
                while True:  # Is not none
                    parent = parent_pointer[0]

                    curr_key = str(level)
                    prev_key = str(level - 1)

                    # Sanity check.
                    if curr_key not in q_cur:
                        # print('No more depth!')
                        break  # No more depth!
                        # Actualy, this should reset the level to the top.

                    # Queue-level pointers.
                    child_queue = q_cur[curr_key]
                    parent_queue = q_cur[prev_key]

                    # Relationship comparison
                    flag = None
                    for child in child_queue:
                        if child in parent[0].children:
                            # First, add it.
                            if not type(parent[1]) is dict:
                                parent[1] = {}
                            parent[1][child.order] = [child, None]
                            child_pointer = parent[1][child.order]
                            # Then, change the pointer.
                            level += 1
                            if str(level) not in q_cur:  # no more depth
                                child_queue.remove(child)
                                level -= 1
                            else:  # continue to next level
                                grandparent_pointer = [parent]
                                parent_pointer = [child_pointer]
                            # First-child only.
                            flag = True
                            break
                    if not flag:  # Has no children
                        # First, remove it.
                        parent_queue.remove(parent[0])
                        # debug_print(title='New Queue {}'.format(steps), data=q_cur)

                        # Then, change the pointer.
                        level -= 1
                        parent_pointer = [grandparent_pointer[0]]
                        grandparent_pointer = [None]
                        # print(level)

                    # if flag:
                    #     print('Next level.')
                    # else:
                    #     print('Previous level.')
                    # print(level, grandparent_pointer, parent_pointer)

                    # This should be the breaking point.
                    # TODO: Test this.

                    if grandparent_pointer[0] is None and parent_pointer[0] is None:
                        break

                    steps += 1

        # Verbosity, thank you.
        # debug_print(title='Elemenet Dictionary', data=e_dict)

    @property
    def owner(self):
        """TODO."""

        return Route.query.get(self.parent)
