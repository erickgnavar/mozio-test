from rest_framework import serializers

from mozio.providers.models import Provider


class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = (
            'name', 'email', 'phone_number',
            'language', 'currency', 'id', 'url',
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api-v1:provider-retrieve-update-destroy',
                'lookup_field': 'id',
            },
        }


class ProviderCreateSerializer(ProviderSerializer):
    """
    Used only for creation becasuse is necessary return the
    token to the provider
    """

    class Meta(ProviderSerializer.Meta):
        fields = ProviderSerializer.Meta.fields + ('token',)
        read_only_fields = ('token',)
