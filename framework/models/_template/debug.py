"""Debugging functions for working on Template."""

from pprint import pprint


class DebugPrint:
    def __init__(self):
        char = '='
        extremity = 10

        # Title-seperator
        title = 'TODO'
        sep_s = char * extremity
        self.title_s = '{} {} {}'.format(sep_s, title, sep_s)

    def element_dict(self, e_dict):
        print('\n' + self.title_s)
        pprint(e_dict, indent=4, width=80)
        print(self.title_s + '\n')

    def queue(self, queue):
        print('\n' + self.title_s)
        pprint(queue, indent=4, width=80)
        print(self.title_s + '\n')
