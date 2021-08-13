from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from src.users import views

router = DefaultRouter()
router.register('messages', views.MessageList, basename='message_list_create')
# router.register('message_detail', views.MessageDetail, basename='message_detail')

# router.register('profile', UserProfileViewSet)

app_name = "users"
urlpatterns = [
    path("", include(router.urls)),
]

# DJ_REST_AUTH authentication, registration and etc. urlpatterns
urlpatterns += [
    # NOTE: DJ_REST_AUTH auth - URLs that do not require a session or valid token
    # path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'), # noqa
    # path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path("auth/login/", LoginView.as_view(), name="rest_login"),

    # NOTE: DJ_REST_AUTH auth - URLs that require a user to be logged in with a valid session / token.
    path("auth/logout/", LogoutView.as_view(), name="rest_logout"),
    # path('user/', UserDetailsView.as_view(), name='rest_user_details'),
    # path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),

    # NOTE: DJ_REST_AUTH registration
    path("registration/", RegisterView.as_view(), name="rest_register"),
    # path('registration/resend-email/', dj_rest_auth_views.RegisterView.as_view()),
    # path('registration/verify-email/', dj_rest_auth_views.ResendEmailVerificationView.as_view()),
]
