from rest_framework import generics

from mozio.providers.models import Provider

from . import permissions, serializers
from .authentication import ProviderTokenAuthentication


class ProviderListCreateView(generics.ListCreateAPIView):

    queryset = Provider.objects.all()
    serializer_class = serializers.ProviderCreateSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.ProviderCreateSerializer
        else:
            return serializers.ProviderSerializer


class ProviderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Provider.objects.all()
    serializer_class = serializers.ProviderSerializer
    lookup_field = 'id'
    authentication_classes = (ProviderTokenAuthentication,)
    permission_classes = (
        permissions.SameProviderPermission,
    )
