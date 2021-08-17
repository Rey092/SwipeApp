from django.urls import include, path
from rest_framework.routers import DefaultRouter

from src.estate import views

router = DefaultRouter()
router.register("complex", views.ComplexViewSet, basename="complex")

app_name = "users"
urlpatterns = [
    path("", include(router.urls)),
]
