from django.urls import include, path
from rest_framework.routers import DefaultRouter

from src.estate import views

router = DefaultRouter()
router.register("complex", views.ComplexViewSet, basename="complex")
router.register("complex_news", views.ComplexNewsViewSet, basename="complex_news")

app_name = "users"
urlpatterns = [
    path("", include(router.urls)),
]
