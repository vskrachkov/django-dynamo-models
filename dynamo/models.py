import collections

from collections import defaultdict
from django.db import models


#### define base model ####
class AbstractModel(models.Model):
    log_date = models.DateTimeField()
    name = models.CharField(max_length=100)
    relation_id = models.IntegerField()

    class Meta:
        abstract = True


#### define utils for model registration and creation ####
def create_model(name, base, attrs=None, meta_attrs=None):
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


QueMap = lambda: defaultdict(lambda: collections.deque([]))
DictMap = lambda: defaultdict(dict)

_models_map = QueMap()
_created_models = DictMap()


def register_model(namespace, name, base, attrs=None, meta_attrs=None):
    _models_map[namespace].append((name, base, attrs, meta_attrs))


def save_model_class(namespace, name, model):
    _created_models[namespace].update({name: model})


def get_model_class(namespace, name):
    return _created_models[namespace].get(name)


def get_registered_models(namespace):
    _models = _models_map[namespace]
    while _models:
        item = _models.pop()
        yield item


def create_registered_models(namespace):
    for name, base, attrs, meta_attrs in get_registered_models(namespace):
        Model = create_model(name, base, attrs, meta_attrs)
        save_model_class(namespace, name, Model)


###### register and create some test models ######
INTERVALS = [1, 20, 60, 120, 360, 1440, 3600, 7600]

for i in INTERVALS:
    register_model(
        'StatAppModelsNamespace',
        f'StatPer{i}Minutes' if i != 1 else 'StatPerMinute',
        AbstractModel,
        attrs={'additional_field': models.IntegerField()},
        meta_attrs={
            'db_table': f'stat_per_{i}_minutes' if i != 1 else 'stat_per_minute'
        }
    )

create_registered_models('StatAppModelsNamespace')
