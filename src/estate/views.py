import rule as rule
from drf_psq import PsqMixin, Rule, psq
from drf_spectacular.utils import extend_schema, PolymorphicProxySerializer
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from src.estate.models import Complex, ComplexNews
from src.estate.paginators import ComplexStandardPagination
from src.estate.permissions import IsComplexOwner
from src.estate.serializers import ComplexSerializer, ComplexNewsSerializer, ComplexNewsRestrictedSerializer
from src.users.permissions import IsDeveloperUser


@extend_schema(tags=["complex"])
class ComplexViewSet(PsqMixin, ModelViewSet):
    pagination_class = ComplexStandardPagination
    queryset = Complex.objects.all()
    serializer_class = ComplexSerializer
    permission_classes = [IsAuthenticated]

    psq_rules = {
        'create': [
            Rule([IsAdminUser], ComplexSerializer),
            Rule([IsDeveloperUser], ComplexSerializer)
        ],
        ('update', 'partial_update', 'destroy'): [
            Rule([IsAdminUser], ComplexSerializer),
            Rule([IsComplexOwner], ComplexSerializer)]
    }

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["complex_news"])
class ComplexNewsViewSet(PsqMixin, ModelViewSet):
    queryset = ComplexNews.objects.all()
    serializer_class = ComplexNewsSerializer
    permission_classes = [IsAuthenticated]

    psq_rules = {
        'create': [
            Rule([IsAdminUser], ComplexNewsSerializer),
            Rule([IsDeveloperUser], ComplexNewsSerializer)
        ],
        ('update', 'partial_update', 'destroy'): [
            Rule([IsAdminUser], ComplexNewsRestrictedSerializer),
            Rule([IsComplexOwner], ComplexNewsRestrictedSerializer)
        ]
    }

    @action(detail=True)
    def get_complex_news(self, request, *args, **kwargs):
        complex_pk = kwargs['pk']
        qs = ComplexNews.objects.filter(complex__pk=complex_pk)
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        complex_pk = request.data['complex']
        if not request.user.complexes.filter(pk=complex_pk).exists():
            raise PermissionDenied()
        else:
            complex_inst = get_object_or_404(Complex, pk=complex_pk)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(complex=complex_inst)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=ComplexNewsRestrictedSerializer)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(request=ComplexNewsRestrictedSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
