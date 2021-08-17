from rest_framework.permissions import BasePermission


class IsDeveloperUser(BasePermission):
    """
    Allows access only to developer users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_developer)
