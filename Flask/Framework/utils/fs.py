#!/usr/bin/env python

"""
anavah.utils.fs
~~~~~~~~~~~~~~~

File-system interface.

:copyright: (c) 2016 Michael Hoyt. <@pr0xmeh>
:license: Anavah.
"""

import os


abs_current = os.path.dirname(os.path.realpath(__file__))
abs_app = os.path.abspath(os.path.join(abs_current, os.pardir))
abs_top = os.path.abspath(os.path.join(abs_app, os.pardir))

abs_fs = {}

# Top-Level
for dir_path, dir_names, file_names in os.walk(abs_top, topdown=False):
    if abs_app in dir_path:
        dir_relative = dir_path.replace(abs_app, '')[1:]
        key_r = '{}/{}'
    elif abs_top in dir_path:
        dir_relative = dir_path.replace(abs_top, '')[1:]
        key_r = '../{}/{}'

    if '__pycache__' in dir_relative:
        continue

    abs_fs[dir_relative] = dir_path
    for file_name in file_names:
        if dir_relative.__len__() > 0:
            key = key_r.format(dir_relative, file_name)
        else:
            key = file_name
        abs_fs[key] = os.path.join(dir_path, file_name)

