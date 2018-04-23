import json

from django.test import TestCase
from django.urls import resolve, reverse
from mixer.backend.django import mixer
from rest_framework.test import (APIClient, APIRequestFactory,
                                 force_authenticate)

from mozio.providers.models import Provider

from .. import views


def create_provider(**kwargs):
    return mixer.blend('providers.Provider', **kwargs)


class ProviderListCreateTestCase(TestCase):

    def setUp(self):
        mixer.cycle(5).blend('providers.Provider')
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.view = views.ProviderListCreateView.as_view()
        self.provider = create_provider()
        self.token = self.provider.token

    def test_match_expected_view(self):
        url = resolve('/api/v1/providers/')
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_create_provider(self):
        request = self.factory.post('/', {
            'name': 'test',
            'email': 'test@test.com',
            'phone_number': '+11231231234',
            'currency': 'USD',
            'language': 'en',
        })
        response = self.view(request)
        self.assertEqual(response.status_code, 201)
        response.render()
        data = json.loads(response.content.decode('utf-8'))
        self.assertIn('token', data)
        self.assertIn('location', response)
        expected_url = reverse('api-v1:provider-retrieve-update-destroy', kwargs={'id': data['id']})
        # this becasuse the response['location'] return the domain and schema
        self.assertIn(expected_url, response['location'])

    def test_list_providers(self):
        request = self.factory.get('/')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        response.render()
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(data), 6)


class ProviderRetrieveUpdateDestroyViewTestCase(TestCase):

    def setUp(self):
        self.provider = mixer.blend('providers.Provider')
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.view = views.ProviderRetrieveUpdateDestroyView.as_view()
        self.provider = create_provider()
        self.token = self.provider.token

    def test_match_expected_view(self):
        url = resolve('/api/v1/providers/1')
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_retrieve(self):
        request = self.factory.get('/')

        response = self.view(request, id=self.provider.id)
        response.render()
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['id'], self.provider.id)

    def test_update(self):
        request = self.factory.put('/', {
            'name': 'new name',
            'email': 'test@test.com',
            'phone_number': '+11231231234',
            'currency': 'USD',
            'language': 'en',
        })
        force_authenticate(request, self.provider, self.token)

        response = self.view(request, id=self.provider.id)
        self.assertEqual(response.status_code, 200)
        response.render()
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['id'], self.provider.id)
        self.provider.refresh_from_db()
        self.assertEqual(self.provider.name, 'new name')

    def test_partial_update(self):
        request = self.factory.patch('/', {
            'name': 'new name',
        })
        force_authenticate(request, self.provider, self.token)

        response = self.view(request, id=self.provider.id)
        self.assertEqual(response.status_code, 200)
        response.render()
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['id'], self.provider.id)
        self.provider.refresh_from_db()
        self.assertEqual(self.provider.name, 'new name')

    def test_destroy(self):
        request = self.factory.delete('/')
        force_authenticate(request, self.provider, self.token)
        response = self.view(request, id=self.provider.id)
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Provider.DoesNotExist):
            Provider.objects.get(id=self.provider.id)
