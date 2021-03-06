from django.test import TestCase
from django.utils.timezone import localtime

from .utils import get_model_class


class TestAutoModels(TestCase):
    def test_a(self):
        Model = get_model_class('StatAppModelsNamespace', 'StatPer7600Minutes')
        NOW = localtime()
        Model.objects.create(
            log_date=NOW, name='some name', relation_id=2, additional_field=2)
        q = Model.objects.filter(
            log_date=NOW, name='some name', relation_id=2, additional_field=2)
        self.assertTrue(q.exists())
