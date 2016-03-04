"""Because writing imports is redundant."""

import importlib
import inspect


def all_models():
    """A list of model-class objects.

    For some reason `__import__('Framework')` doesn't contain
    `models` as a member, so it has to be import-ed absolutely as such.
    """

    models = []
    foo = __import__('Framework.models').models
    for name, obj in inspect.getmembers(foo):
        if inspect.isclass(obj):
            models.append(obj)
    return models
