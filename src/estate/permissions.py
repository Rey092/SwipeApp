from rest_framework.permissions import BasePermission, IsAuthenticated

from src.estate.models import (
    Apartment,
    ApartmentGalleryImage,
    Complex,
    ComplexGalleryImage,
    ComplexNews,
)
from src.users.permissions import IsDeveloperUser


class IsComplexOwner(IsDeveloperUser):
    """
    Allows access only to complex owner.
    Supported models: Complex, ComplexNews, ComplexGalleryImage
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Complex):
            return bool(request.user.complexes.filter(pk=obj.pk).exists())
        elif isinstance(obj, (ComplexNews, ComplexGalleryImage)):
            return bool(request.user.complexes.filter(pk=obj.complex.pk).exists())
        else:
            return False


class IsApartmentOwner(IsAuthenticated):
    """
    Allows access only to apartment owner.
    Supported models: Apartment
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Apartment):
            return bool(request.user.apartments.filter(pk=obj.pk).exists())
        elif isinstance(obj, ApartmentGalleryImage):
            return bool(request.user.apartments.filter(pk=obj.apartment.pk).exists())
        else:
            return False
