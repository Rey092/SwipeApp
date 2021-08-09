from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists
from dj_rest_auth.serializers import PasswordResetSerializer, LoginSerializer
from rest_framework import serializers

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import Serializer


class AuthLoginSerializer(LoginSerializer):
    email = None

# class CustomPasswordResetSerializer(PasswordResetSerializer):
#     def get_email_options(self):
#         return {
#             'subject_template_name': 'registration/password_reset_subject.txt',
#             'email_template_name': 'registration/password_reset_message.txt',
#             'html_email_template_name': 'registration/'
#                                     'password_reset_message.html',
#             'extra_email_context': {
#                 'pass_reset_obj': self.your_extra_reset_obj
#             }
#         }


class HelloSerializer(Serializer):
    """Serializes a name field for testing our APIView"""
    name = CharField(max_length=15)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ApiRegisterSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    # def validate_username(self, username):
    #     username = get_adapter().clean_username(username)
    #     return username

    @staticmethod
    def validate_email(email):
        email = get_adapter().clean_email(email)
        if True:
            # if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _('A user is already registered with this e-mail address.'),
                )
        return email

    @staticmethod
    def validate_password1(password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'phone': self.validated_data.get('phone', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        try:
            adapter.clean_password(self.cleaned_data['password1'], user=user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                detail=serializers.as_serializer_error(exc)
            )
        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user
