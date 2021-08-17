from rest_framework.permissions import BasePermission, IsAuthenticated

from src.users.permissions import IsDeveloperUser


class IsComplexOwner(IsDeveloperUser):
    """
    Allows access only to complex owner.
    Support models: Complex, ComplexNews
    """

    def has_object_permission(self, request, view, obj):
        print(1)
        print(request.data, obj)
        return bool(request.user.complexes.filter(pk=obj.pk).exists())
