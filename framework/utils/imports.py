"""Because writing imports is redundant."""

import importlib
import inspect


def all_models():
    """A list of model-class objects.

    For some reason `__import__('Framework')` doesn't contain
    `models` as a member, so it has to be import-ed absolutely as such.
    """

    models = []
    namespace = __import__('framework').models

    for name, obj in inspect.getmembers(namespace):
        if inspect.ismodule(obj):
            for _name, _obj in inspect.getmembers(obj):
                if inspect.isclass(_obj):
                    if _obj not in models:
                        models.append(_obj)
    return models
