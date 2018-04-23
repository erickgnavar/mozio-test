from django.test import TestCase
from mixer.backend.django import mixer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.test import APIRequestFactory

from ..authentication import ProviderTokenAuthentication


class ProviderTokenAuthenticationTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.provider = mixer.blend('providers.Provider')
        self.authentication = ProviderTokenAuthentication()

    def test_token_not_found(self):
        request = self.factory.get('/')
        self.assertIsNone(self.authentication.authenticate(request))

    def test_provider_token_does_not_exist(self):
        request = self.factory.get('/', HTTP_X_API_TOKEN='another token')
        with self.assertRaises(AuthenticationFailed):
            self.assertIsNone(self.authentication.authenticate(request))

    def test_success(self):
        request = self.factory.get('/', HTTP_X_API_TOKEN=self.provider.token)
        provider, token = self.authentication.authenticate(request)
        self.assertEqual(provider.id, self.provider.id)
        self.assertEqual(token, self.provider.token)
