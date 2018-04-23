import json

from django.test import TestCase
from django.urls import resolve, reverse
from mixer.backend.django import mixer
from rest_framework.test import (APIClient, APIRequestFactory,
                                 force_authenticate)

from mozio.areas.models import ServiceArea
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


class ServiceAreaListCreateTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.view = views.ServiceAreaListCreateView.as_view()
        self.provider = create_provider()
        self.token = self.provider.token

    def test_match_expected_view(self):
        url = resolve('/api/v1/service-areas/')
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_create(self):
        request = self.factory.post('/', {
            'name': 'sample area',
            'price': '12.12',
            'polygon': 'POLYGON ((13.1 16.6, 7.1 17.6, 9.8 14.4, 13.1 16.6))',
        })
        force_authenticate(request, self.provider, self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, 201)
        response.render()
        data = json.loads(response.content.decode('utf-8'))
        service_area = ServiceArea.objects.get(id=data['id'])
        self.assertEqual(service_area.provider_id, self.provider.id)

    def test_list(self):
        mixer.cycle(5).blend('areas.ServiceArea', polygon='POLYGON ((1.1 1.1, 1.2 1.2, 1.3 1.3, 1.1 1.1))')
        request = self.factory.get('/')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        response.render()
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(data['features']), 5)


class ServiceAreaRetrieveUpdateDestroyViewTestCase(TestCase):

    def setUp(self):
        self.provider = create_provider()
        self.service_area = mixer.blend(
            'areas.ServiceArea',
            polygon='POLYGON ((1.1 1.1, 1.2 1.2, 1.3 1.3, 1.1 1.1))',
            provider=self.provider,
        )
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.view = views.ServiceAreaRetrieveUpdateDestroyView.as_view()
        self.token = self.provider.token

    def test_match_expected_view(self):
        url = resolve('/api/v1/service-areas/1')
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_retrieve(self):
        request = self.factory.get('/')

        response = self.view(request, id=self.service_area.id)
        response.render()
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['id'], self.service_area.id)

    def test_update(self):
        request = self.factory.put('/', {
            'name': 'new area',
            'price': '12.12',
            'polygon': 'POLYGON ((1.1 1.1, 1.2 1.2, 1.3 1.3, 1.1 1.1))',
        })
        force_authenticate(request, self.provider, self.token)

        response = self.view(request, id=self.service_area.id)
        self.assertEqual(response.status_code, 200)
        response.render()
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['id'], self.service_area.id)
        self.service_area.refresh_from_db()
        self.assertEqual(self.service_area.name, 'new area')

    def test_partial_update(self):
        request = self.factory.patch('/', {
            'name': 'new name',
        })
        force_authenticate(request, self.provider, self.token)

        response = self.view(request, id=self.service_area.id)
        self.assertEqual(response.status_code, 200)
        response.render()
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['id'], self.service_area.id)
        self.service_area.refresh_from_db()
        self.assertEqual(self.service_area.name, 'new name')

    def test_destroy(self):
        request = self.factory.delete('/')
        force_authenticate(request, self.provider, self.token)
        response = self.view(request, id=self.service_area.id)
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(ServiceArea.DoesNotExist):
            ServiceArea.objects.get(id=self.service_area.id)
