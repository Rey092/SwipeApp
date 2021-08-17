from rest_framework.permissions import BasePermission, IsAuthenticated

from src.users.permissions import IsDeveloperUser


class IsComplexOwner(IsDeveloperUser):

    def has_object_permission(self, request, view, obj):
        return bool(request.user.complexes.filter(pk=obj.pk).exists())
