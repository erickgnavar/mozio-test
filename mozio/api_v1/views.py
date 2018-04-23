from django.contrib.gis.geos import Point
from rest_framework import generics

from mozio.areas.models import ServiceArea
from mozio.providers.models import Provider

from . import forms, permissions, serializers
from .authentication import ProviderTokenAuthentication


SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class ProviderListCreateView(generics.ListCreateAPIView):

    queryset = Provider.objects.all()
    serializer_class = serializers.ProviderCreateSerializer

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return serializers.ProviderSerializer
        else:
            return serializers.ProviderCreateSerializer


class ProviderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Provider.objects.all()
    serializer_class = serializers.ProviderSerializer
    lookup_field = 'id'
    authentication_classes = (ProviderTokenAuthentication,)
    permission_classes = (
        permissions.IsOwnerOrReadOnly,
    )


class ServiceAreaListCreateView(generics.ListCreateAPIView):

    serializer_class = serializers.ServiceAreaSerializer

    def get_queryset(self):
        qs = ServiceArea.objects.select_related('provider')
        form = forms.ServiceAreaForm(self.request.GET)
        if form.is_valid():
            point = Point(form.cleaned_data['lng'], form.cleaned_data['lat'])
            qs = qs.filter(polygon__contains=point)
        return qs

    @property
    def authentication_classes(self):
        if self.request.method in SAFE_METHODS:
            return tuple()
        else:
            return (ProviderTokenAuthentication,)

    def perform_create(self, serializer):
        # The user is an instance of Provider
        serializer.save(provider=self.request.user)


class ServiceAreaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    queryset = ServiceArea.objects.all()
    serializer_class = serializers.ServiceAreaSerializer
    lookup_field = 'id'
    permission_classes = (
        permissions.IsOwnerOrReadOnly,
    )

    @property
    def authentication_classes(self):
        if self.request.method in SAFE_METHODS:
            return tuple()
        else:
            return (ProviderTokenAuthentication,)
