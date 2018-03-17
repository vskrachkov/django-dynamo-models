import collections
from collections import defaultdict


QueMap = lambda: defaultdict(lambda: collections.deque([]))
DictMap = lambda: defaultdict(dict)
_models_map = QueMap()
_created_models = DictMap()


def get_model_class(namespace, name):
    return _created_models[namespace].get(name)


def register_model(namespace, name, base, attrs=None, meta_attrs=None):
    _models_map[namespace].append((name, base, attrs, meta_attrs))


def create_registered_models(namespace):
    for name, base, attrs, meta_attrs in _get_registered_models(namespace):
        Model = _create_model(name, base, attrs, meta_attrs)
        _save_model_class(namespace, name, Model)


def _create_model(name, base, attrs=None, meta_attrs=None):
    if not meta_attrs:
        meta_attrs = {}

    Meta = type('Meta', (object,), meta_attrs)

    if not attrs:
        attrs = {}

    if not attrs.get('__module__'):
        attrs['__module__'] = __name__

    attrs.update({'Meta': Meta})

    Model = type(name, (base,), attrs)

    return Model


def _save_model_class(namespace, name, model):
    _created_models[namespace].update({name: model})


def _get_registered_models(namespace):
    _models = _models_map[namespace]
    while _models:
        item = _models.pop()
        yield item
