from django.db import models

from .utils import register_model, create_registered_models


class AbstractModel(models.Model):
    log_date = models.DateTimeField()
    name = models.CharField(max_length=100)
    relation_id = models.IntegerField()

    class Meta:
        abstract = True


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
