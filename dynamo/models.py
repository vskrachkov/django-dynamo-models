import collections

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


_models = collections.deque([])


def register_model(name, base, attrs=None, meta_attrs=None):
    _models.append((name, base, attrs, meta_attrs))


def get_registered_models():
    while _models:
        yield _models.pop()


def create_registered_models():
    for name, base, attrs, meta_attrs in get_registered_models():
        create_model(name, base, attrs, meta_attrs)


###### register and create some test models ######
INTERVALS = [1, 20, 60, 120, 360, 1440, 3600]

for i in INTERVALS:
    register_model(
        f'StatPer{i}Minutes' if i != 1 else 'StatPerMinute',
        AbstractModel,
        attrs={'additional_field': models.IntegerField()},
        meta_attrs={
            'db_table': f'stat_per_{i}_minutes' if i != 1 else 'stat_per_minute'
        }
    )

create_registered_models()
