import instance as instance
from django.db.models import Max
from django_filters.rest_framework import DjangoFilterBackend
from drf_psq import PsqMixin, Rule
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from src.estate.filters import ApartmentFilter
from src.estate.models import (
    Advertisement,
    Apartment,
    ApartmentGalleryImage,
    Complaint,
    Complex,
    ComplexDocument,
    ComplexGalleryImage,
    ComplexNews,
)
from src.estate.permissions import IsApartmentOwner, IsComplexOwner
from src.estate.serializers import (
    AdvertisementSerializer,
    ApartmentDeveloperSerializer,
    ApartmentGalleryImageRestrictedSerializer,
    ApartmentGalleryImageSerializer,
    ApartmentRestrictedSerializer,
    ApartmentSerializer,
    ComplaintRestrictedSerializer,
    ComplaintSerializer,
    ComplexDocumentRestrictedSerializer,
    ComplexDocumentSerializer,
    ComplexGalleryImageRestrictedSerializer,
    ComplexGalleryImageSerializer,
    ComplexNewsRestrictedSerializer,
    ComplexNewsSerializer,
    ComplexSerializer,
)
from src.estate.services.complex_services import create_complex_related_object
from src.users.models import Filter
from src.users.permissions import IsDeveloperUser


@extend_schema(tags=["complex"])
class ComplexViewSet(PsqMixin, ModelViewSet):
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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        complex_count = queryset.count()
        return Response({'data': serializer.data,
                         "complex_count": complex_count})

    def retrieve(self, request, *args, **kwargs):
        complex_obj = self.get_object()
        serializer = self.get_serializer(complex_obj)
        complex_max_corpus = Apartment.objects.filter(complex=complex_obj). \
            aggregate(complex_max_corpus=Max('corpus'))['complex_max_corpus']
        return Response({'data': serializer.data,
                        "complex_max_corpus": complex_max_corpus})

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
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["complex"]

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

    def create(self, request, *args, **kwargs):
        return create_complex_related_object(self, request, *args, **kwargs)

    @extend_schema(request=ComplexNewsRestrictedSerializer)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(request=ComplexNewsRestrictedSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


@extend_schema(tags=["complex_gallery"])
class ComplexGalleryImageViewSet(PsqMixin, ModelViewSet):
    queryset = ComplexGalleryImage.objects.all()
    serializer_class = ComplexGalleryImageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["complex"]

    psq_rules = {
        'create': [
            Rule([IsAdminUser], ComplexGalleryImageSerializer),
            Rule([IsDeveloperUser], ComplexGalleryImageSerializer)
        ],
        ('update', 'partial_update', 'destroy'): [
            Rule([IsAdminUser], ComplexGalleryImageRestrictedSerializer),
            Rule([IsComplexOwner], ComplexGalleryImageRestrictedSerializer)]
    }

    def create(self, request, *args, **kwargs):
        return create_complex_related_object(self, request, *args, **kwargs)

    @extend_schema(request=ComplexGalleryImageRestrictedSerializer)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(request=ComplexGalleryImageRestrictedSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


@extend_schema(tags=["complex_document"])
class ComplexDocumentViewSet(PsqMixin, ModelViewSet):
    queryset = ComplexDocument.objects.all()
    serializer_class = ComplexDocumentSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["complex"]

    psq_rules = {
        'create': [
            Rule([IsAdminUser], ComplexDocumentSerializer),
            Rule([IsDeveloperUser], ComplexDocumentSerializer)
        ],
        ('update', 'partial_update', 'destroy'): [
            Rule([IsAdminUser], ComplexDocumentRestrictedSerializer),
            Rule([IsComplexOwner], ComplexDocumentRestrictedSerializer)]
    }

    def create(self, request, *args, **kwargs):
        return create_complex_related_object(self, request, *args, **kwargs)


@extend_schema(tags=["apartment"])
class ApartmentViewSet(PsqMixin, ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ApartmentFilter

    psq_rules = {
        'create': [
            Rule([IsAuthenticated], ApartmentRestrictedSerializer)],
        ('update', 'partial_update'): [
            Rule([IsAdminUser], ApartmentSerializer),
            Rule([IsDeveloperUser], ApartmentDeveloperSerializer),
            Rule([IsApartmentOwner], ApartmentRestrictedSerializer)],
        'destroy': [
            Rule([IsAdminUser], ApartmentSerializer),
            Rule([IsApartmentOwner], ApartmentRestrictedSerializer)],
    }

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# noinspection DuplicatedCode
@extend_schema(tags=["apartment_gallery"])
class ApartmentGalleryImageViewSet(PsqMixin, ModelViewSet):
    queryset = ApartmentGalleryImage.objects.all()
    serializer_class = ApartmentGalleryImageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    psq_rules = {
        ('update', 'partial_update', 'destroy'): [
            Rule([IsAdminUser], ApartmentGalleryImageRestrictedSerializer),
            Rule([IsApartmentOwner], ApartmentGalleryImageRestrictedSerializer)]
    }

    @action(detail=True)
    def get_apartment_gallery(self, request, *args, **kwargs):
        apartment_pk = kwargs['pk']
        qs = ApartmentGalleryImage.objects.filter(apartment__pk=apartment_pk)
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=ApartmentGalleryImageRestrictedSerializer)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(request=ApartmentGalleryImageRestrictedSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


@extend_schema(tags=["apartment_complaint"])
class ComplaintViewSet(PsqMixin, ModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]

    psq_rules = {
        'create': [
            Rule([IsAuthenticated], ComplaintRestrictedSerializer)],
        ('list', 'retrieve', 'update', 'partial_update', 'destroy'): [
            Rule([IsAdminUser], ComplaintSerializer)],
    }

    @extend_schema(request=ComplaintRestrictedSerializer)
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["apartment_advertisement"])
class AdvertisementViewSet(PsqMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin,
                           GenericViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated]

    psq_rules = {
        'list': [
            Rule([IsAdminUser], AdvertisementSerializer)],
        ('retrieve', 'update', 'partial_update', 'destroy'): [
            Rule([IsAdminUser], AdvertisementSerializer)],
    }
