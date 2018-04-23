from django.test import TestCase
from mixer.backend.django import mixer


from ..models import Provider


class UserTestCase(TestCase):

    def test_str(self):
        provider = Provider(name='test')
        self.assertEqual(str(provider), 'test')

    def test_regenerate_token(self):
        provider = mixer.blend('providers.Provider')
        old_token = provider.token
        provider.generate_token()
        self.assertNotEqual(provider.token, old_token)
