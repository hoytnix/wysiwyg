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


    e_dict = {}
    visited = []
    for top_key in queue:
        # First
        e_dict[top_key] = {}

        # Convenience pointers
        r_cur = e_dict[top_key]
        q_cur = queue[top_key]

        # Populate first for operation.
        for e_cur in q_cur[0]:
            r_cur[e_cur.order] = [e_cur, None]

        # Loop for each top-level element.
        for te_key in r_cur:
            te_cur = r_cur[te_key]  # Top-element pointer
            # It looks like I have two top-element pointers here.

            # Tree traversal
            level = 1
            grandparent_pointer = [None]
            parent_pointer = [te_cur]
            while True:
                # Step-counter.
                steps = 0

                # Level-keys.
                curr_key = (level)
                prev_key = (level - 1)

                # Sanity check.
                if curr_key not in q_cur:
                    print('No more depth!')
                    break  # No more depth!
                    # Actualy, this should reset the level to the top.

                # Pointers.
                parent = parent_pointer[0]
                child_queue = q_cur[curr_key]
                parent_queue = q_cur[prev_key]

                # Relationship comparison
                flag = None
                for child in child_queue:
                    if child in parent[0].children:

                        # First, change None to Dict.
                        if not type(parent[1]) is dict:
                            parent[1] = {}

                        # Append the new child.
                        parent[1][child.order] = [child, None]
                        child_pointer = parent[1][child.order]

                        # Check for more depth.
                        level += 1
                        if str(level) not in q_cur:  # no more depth
                            child_queue.remove(child)
                            level -= 1
                        else:  # continue to next level
                            grandparent_pointer = [parent]
                            parent_pointer = [child_pointer]

                        # Perform on one child only.
                        flag = True
                        break

                if not flag:  # Has no children
                    # First, remove it.
                    parent_queue.remove(parent[0])
                    debug_print(q_cur, title='QUEUE {}'.format(steps))

                    # Then, change the pointer.
                    level -= 1
                    parent_pointer = [grandparent_pointer[0]]
                    grandparent_pointer = [None]

                # This should be the breaking point.
                # TODO: Test this.
                if grandparent_pointer[0] is None and parent_pointer[0] is None:
                    break

                # Increment step.
                steps += 1

    # Verbosity, thank you.
    debug_print(e_dict, title='ELEMENT DICT')

    return e_dict
