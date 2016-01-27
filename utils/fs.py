#!/usr/bin/env python

"""
anavah.utils.fs
~~~~~~~~~~~~~~~

File-system interface.

:copyright: (c) 2016 Michael Hoyt. <@pr0xmeh>
:license: Anavah.
"""

import os

'''
Anavah
|- Controller (app)
|-- utils     (current)
|-- templates 
'''

abs_current = os.path.dirname(os.path.realpath(__file__))
abs_app = os.path.abspath(os.path.join(abs_current, os.pardir))

abs_templates = os.path.join(abs_current, 'templates')

abs_fs = {}
for dirpath, dirnames, filenames in os.walk(abs_app):
    for file_name in filenames:
        key = '.'.join(file_name.split('.')[:-1]) # file-name without extension
        abs_fs[key] = os.path.join(dirpath, file_name)


