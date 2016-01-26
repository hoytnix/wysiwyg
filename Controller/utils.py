#!/usr/bin/env python

"""
utils
~~~~~

Flask toolbox.

:copyright: (c) 2016 Michael Hoyt. <@pr0xmeh>
:license: Anavah. 
"""

import os
import importlib
import inspect
import re

import unidecode


abs_current = os.path.dirname(os.path.realpath(__file__))
abs_parent  = os.path.abspath(os.path.join(abs_current, os.pardir))
abs_templates = os.path.join(abs_parent, 'templates')
abs_fs = {}
for dirpath, dirnames, filenames in os.walk(abs_current):
    for file_name in filenames:
        key = '.'.join(file_name.split('.')[:-1]) # file-name without extension
        abs_fs[key] = os.path.join(dirpath, file_name)

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def all_models():
    '''Returns a list of model-class objects.

    For some reason `__import__('flask_extensions')` doesn't contain
    `models` as a member, so it has to be import-ed absolutely as such.
    '''

    models = []
    foo = __import__('flask_extensions.models').models
    for name, obj in inspect.getmembers(foo):
        if inspect.isclass(obj):
            models.append(obj)
    return models


def slugify(text, delim=u'-'):
    '''Returns an ASCII-only slug.
    Taken from FlaskBB. <@shanks>

    :param text: Text to slugify.
    :param delim: Default '-'. Delimiter for whitespace.
    '''

    text = unidecode.unidecode(text)
    result = []
    for word in _punct_re.split(text.lower()):
        result.append(word)
    return delim.join(result)




