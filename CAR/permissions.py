from rest_framework import permissions

class IsSuperuserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only superusers to perform POST requests.
    Everyone else can perform GET requests.
    """

    def has_permission(self, request, view):
        # Allow GET, HEAD, or OPTIONS requests for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # only Super user
        return request.user and request.user.is_superuser
