from rest_framework import permissions


class SameProviderPermission(permissions.BasePermission):
    """
    Check if the current provider is the owner of the resource
    Only apply for the /providers/ endpoint
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Using ProviderTokenAuthentication the request.user object is an instance of Provider
        return obj == request.user
