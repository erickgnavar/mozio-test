from rest_framework import authentication, exceptions

from mozio.providers.models import Provider


class ProviderTokenAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        token = request.META.get('HTTP_X_API_TOKEN')
        if not token:
            return None

        try:
            provider = Provider.objects.get(token=token)
        except Provider.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such provider')

        return (provider, token)
