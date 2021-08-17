from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers

from src.users.models import Message, File, Contact, Subscription, Notary, ServiceCenter

User = get_user_model()


# region AUTH


class AuthLoginSerializer(LoginSerializer):  # noqa
    #  Exclude email field from Token Authentication.
    username = None


class AuthRegisterSerializer(RegisterSerializer):  # noqa
    #  Exclude email field from Token Authentication.
    username = None
    first_name = serializers.CharField(
        max_length=150,
        min_length=2,
        required=True,
    )
    last_name = serializers.CharField(
        max_length=150,
        min_length=2,
        required=True,
    )

    def get_cleaned_data(self):
        return {
            "username": self.validated_data.get("username", ""),
            "password1": self.validated_data.get("password1", ""),
            "email": self.validated_data.get("email", ""),
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
        }

    def save(self, request):
        user = super().save(request)

        # logger.debug("[GroupProfile-Manager] Manager user registration #{}: {}".format(user.id, user.email))
        # group_prof_obj.join(user=user, role='manager')

        return user


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
#
#
# class ApiRegisterSerializer(serializers.Serializer):
#     def update(self, instance, validated_data):
#         pass
#
#     def create(self, validated_data):
#         pass
#
#     username = serializers.CharField(required=True)
#     email = serializers.EmailField(required=True)
#     password1 = serializers.CharField(write_only=True)
#     password2 = serializers.CharField(write_only=True)
#
#     # def validate_username(self, username):
#     #     username = get_adapter().clean_username(username)
#     #     return username
#
#     @staticmethod
#     def validate_email(email):
#         email = get_adapter().clean_email(email)
#         if True:
#             # if allauth_settings.UNIQUE_EMAIL:
#             if email and email_address_exists(email):
#                 raise serializers.ValidationError(
#                     _("A user is already registered with this e-mail address.")
#                 )
#         return email
#
#     @staticmethod
#     def validate_password1(password):
#         return get_adapter().clean_password(password)
#
#     def validate(self, data):
#         if data["password1"] != data["password2"]:
#             raise serializers.ValidationError(
#                 _("The two password fields didn't match.")
#             )
#         return data
#
#     def custom_signup(self, request, user):
#         pass
#
#     def get_cleaned_data(self):
#         return {
#             "phone": self.validated_data.get("phone", ""),
#             "password1": self.validated_data.get("password1", ""),
#             "email": self.validated_data.get("email", ""),
#         }
#
#     def save(self, request):
#         adapter = get_adapter()
#         user = adapter.new_user(request)
#         self.cleaned_data = self.get_cleaned_data()
#         user = adapter.save_user(request, user, self, commit=False)
#         try:
#             adapter.clean_password(self.cleaned_data["password1"], user=user)
#         except DjangoValidationError as exc:
#             raise serializers.ValidationError(
#                 detail=serializers.as_serializer_error(exc)
#             )
#         user.save()
#         self.custom_signup(request, user)
#         setup_user_email(request, user, [])
#         return user
#

# endregion AUTH

# region MESSAGES


class FileUploadSerializer(serializers.ModelSerializer):  # noqa
    file = serializers.FileField()

    class Meta:
        model = File
        fields = ["file", "message"]
        read_only_fields = ["message"]

    def create(self, **validated_data):
        file = validated_data.pop("file")
        message = validated_data.pop("message")

        obj = File.objects.create(file=file, message=message)
        return obj


@extend_schema_serializer(
    exclude_fields=[
        "sender",
    ],  # schema ignore these fields
    examples=[
        OpenApiExample(
            "Example",
            # summary='short summary',
            # description='longer description',
            value={
                "recipient": 0,
                "text": "string",
                "is_feedback": False,
            },
            request_only=True,  # signal that example only applies to requests
            response_only=False,  # signal that example only applies to responses
        ),
    ],
)
class MessageSerializer(serializers.ModelSerializer):
    uploaded_files = serializers.ListField(
        child=serializers.FileField(write_only=True), write_only=True
    )
    message_files = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Message
        fields = [
            "id",
            "sender",
            "recipient",
            "text",
            "is_feedback",
            "uploaded_files",
            "message_files",
        ]
        read_only_fields = ["sender"]

    def create(self, validated_data):
        files = validated_data.pop("uploaded_files")
        message = Message.objects.create(**validated_data)

        for file in files:
            serializer = FileUploadSerializer(
                data={"message": message.id, "file": file}
            )
            if serializer.is_valid():
                serializer.create(message=message, file=file)
            else:
                raise serializers.ValidationError("file data is invalid")
        return message


class MessageRecipientUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "avatar", "first_name", "last_name"]


# endregion MESSAGES

# region USERS
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "avatar",
            "forward_to_agent",
            "notification_type",
            "favorite_apartments",
            "favorite_complex",
        ]
        read_only_fields = [
            "is_staff",
            "is_active",
            "is_blacklisted",
            "is_developer",
            "date_joined",
        ]


class UserAgentContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "phone", "email"]


class UserSubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(write_only=True)
    token = serializers.CharField(write_only=True)
    is_passed = serializers.BooleanField(write_only=True)

    class Meta:
        model = Subscription
        fields = [
            "is_active",
            "created",
            "expiration",
            "auto_renewal",
            "token",
            "is_passed",
            "user",
        ]
        read_only_fields = ["is_active", "created", "expiration", "auto_renewal"]


# endregion USERS

# region OTHER_STAFF


class NotarySerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(max_length=None, use_url=False, allow_null=True, required=False)

    class Meta:
        model = Notary
        fields = ["id", "first_name", "last_name", "phone", "email", "address", "avatar"]


class ServiceCenterSerializer(serializers.ModelSerializer):
    icon = serializers.ImageField(max_length=None, use_url=False, allow_null=True, required=False)

    class Meta:
        model = ServiceCenter
        fields = ["id", "address", "name", "map_lat", "map_lng", "icon"]
