from django.urls import include, path
from rest_framework.routers import DefaultRouter

from src.estate import views

router = DefaultRouter()
router.register("complex", views.ComplexViewSet, basename="complex")
router.register("complex_news", views.ComplexNewsViewSet, basename="complex_news")
router.register("complex_gallery", views.ComplexGalleryImageViewSet, basename="complex_gallery")
router.register("complex_document", views.ComplexDocumentViewSet, basename="complex_document")

router.register("apartment", views.ApartmentViewSet, basename="apartment")
router.register("apartment_gallery", views.ApartmentGalleryImageViewSet, basename="apartment_gallery")
router.register("apartment_complaint", views.ComplaintViewSet, basename="apartment_complaint")
router.register("apartment_advertisement", views.AdvertisementViewSet, basename="apartment_advertisement")


app_name = "users"
urlpatterns = [
    path("", include(router.urls)),
]
