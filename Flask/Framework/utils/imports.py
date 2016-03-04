#!/usr/bin/env python

"""
anavah.utils.imports
~~~~~~~~~~~~~~~~~~~~

Because writing imports is redundant.

:copyright: (c) 2016 Michael Hoyt. <@pr0xmeh>
:license: Anavah.
"""

import importlib
import inspect


def all_models():
    '''Returns a list of model-class objects.

    For some reason `__import__('Framework')` doesn't contain
    `models` as a member, so it has to be import-ed absolutely as such.
    '''

    models = []
    foo = __import__('Framework.models').models
    for name, obj in inspect.getmembers(foo):
        if inspect.isclass(obj):
            models.append(obj)
    return models
