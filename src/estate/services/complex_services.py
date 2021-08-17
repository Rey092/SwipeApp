from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.response import Response

from src.estate.models import Complex


def get_complex_instance(request):
    if not request.user.is_authenticated:
        raise NotAuthenticated()

    try:
        complex_pk = request.data['complex']
    except KeyError:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    if not request.user.complexes.filter(pk=complex_pk).exists():
        raise PermissionDenied()

    complex_inst = Complex.objects.get(pk=complex_pk)

    return complex_inst


def create_complex_related_object(self, request, *args, **kwargs):
    serializer = self.serializer_class(data=request.data, context={'user': request.user})
    serializer.is_valid(raise_exception=True)
    complex_obj = Complex.objects.get(pk=request.data['complex'])
    serializer.save(complex=complex_obj)
    return Response(serializer.data, status=status.HTTP_200_OK)
