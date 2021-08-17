from rest_framework.permissions import BasePermission, IsAuthenticated


class IsDeveloperUser(BasePermission):
    """
    Allows access only to developer users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_developer)


class IsFilterOwner(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return bool(request.user.user_filters.filter(pk=obj.pk).exists())
