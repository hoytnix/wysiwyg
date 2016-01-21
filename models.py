#!/usr/bin/env python

"""
models
~~~~~~

(M)VC.

:copyright: (c) 2016 Michael Hoyt. <@pr0xmeh>
:license: Anavah.
"""

from random import choice


'''
    Randomized data models.
'''

bootstrap_template = choice([
    'cerulean', 'cosmo', 'cyborg', 'darkly', 'flatly', 'journal', 'lumen',
    'paper', 'readable', 'sandstone', 'simplex', 'slate', 'spacelab',
    'superhero', 'united', 'yeti'
])

user = choice([
    {
        'name': 'Oloty'
    }
])



'''
    Key-values
'''

page_titles = {
    # Pages
    'index': None,

    # BBS
    'apps/bbs/index': 'BBS',

    # Blog
    'apps/blog/index': 'Blog',

    # Store
    'apps/store/index': 'Store',

    # Support
    'apps/support/index': 'Support',
    'apps/support/faq': 'FAQs',
    'apps/support/issues': 'Issues',

    # Wiki
    'apps/wiki/index': 'Wiki',

    # UCP
    'ucp/index': 'UCP',

}


