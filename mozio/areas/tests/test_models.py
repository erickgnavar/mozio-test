from django.test import TestCase

from ..models import ServiceArea


class ServiceAreaTestCase(TestCase):

    def test_str(self):
        service_area = ServiceArea(name='test')
        self.assertEqual(str(service_area), 'test')
