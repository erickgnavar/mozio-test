from django.test import TestCase
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory

from ..permissions import IsOwnerOrReadOnly


class IsOwnerOrReadOnlyTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.provider = mixer.blend('providers.Provider')
        self.permission = IsOwnerOrReadOnly()

    def test_allows_for_safe_methods(self):
        request = self.factory.get('/')
        self.assertTrue(self.permission.has_object_permission(request, None, None))

        request = self.factory.options('/')
        self.assertTrue(self.permission.has_object_permission(request, None, None))

        request = self.factory.head('/')
        self.assertTrue(self.permission.has_object_permission(request, None, None))

    def test_resource_belongs_to_provider(self):
        request = self.factory.post('/')
        request.user = self.provider
        self.assertTrue(self.permission.has_object_permission(request, None, self.provider))

    def test_resource_does_not_belongs_to_provider(self):
        request = self.factory.post('/')
        request.user = self.provider
        another_provider = mixer.blend('providers.Provider')
        self.assertFalse(self.permission.has_object_permission(request, None, another_provider))
