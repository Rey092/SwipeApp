from drf_psq import PsqMixin, Rule
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from src.estate.models import Complex, ComplexNews
from src.estate.paginators import ComplexStandardPagination
from src.estate.permissions import IsComplexOwner
from src.estate.serializers import ComplexSerializer
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


@extend_schema(tags=["complex"])
class ComplexViewSet(PsqMixin, ModelViewSet):
    queryset = ComplexNews.objects.all()
    serializer_class = ComplexNewsSerializer
    permission_classes = [IsAdminUser]

    psq_rules = {
        ('list', 'retrieve'): [
            Rule([IsAuthenticated], ComplexSerializer),
        ],
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
