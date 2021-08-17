import datetime

from dateutil.tz import UTC
from django.contrib.auth import get_user_model
from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from src.users.models import Contact, Message, Notary, ServiceCenter, Subscription, Filter
from src.users.permissions import IsFilterOwner
from src.users.serializers import (
    MessageRecipientUserSerializer,
    MessageSerializer,
    NotarySerializer,
    ServiceCenterSerializer,
    UserAgentContactSerializer,
    UserProfileSerializer,
    UserSubscriptionSerializer,
)

User = get_user_model()


# noinspection PyMethodMayBeStatic
@extend_schema(tags=["messages"])
class MessageList(ViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser]

    def list(self, request):
        """Returns a list of all Users that received messages or sent them to current User."""

        queryset = (
            User.objects.prefetch_related("received_messages", "sent_messages")
                .filter(Q(received_messages__sender=request.user) | Q(sent_messages__recipient=request.user)).distinct()
        )
        serializer = MessageRecipientUserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Create a new message where sender is current User and recipient is target User."""

        files = request.data.get("files", None)

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save(sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        """Returns a list of all Messages between current User and target User."""

        queryset = (
            Message.objects.select_related("sender", "recipient").filter(
                Q(sender=request.user, recipient__pk=pk)
                | Q(sender__pk=pk, recipient=request.user)
            ).order_by("-created")
        )
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# noinspection PyMethodMayBeStatic,DuplicatedCode
@extend_schema(tags=["user_profile"])
class UserProfileViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer
    parser_classes = [MultiPartParser]

    @action(detail=False)
    def get_current_user_data(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def update_current_user_data(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# noinspection PyMethodMayBeStatic,DuplicatedCode
@extend_schema(tags=["user_profile"])
class UserAgentContactViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserAgentContactSerializer

    @action(detail=False)
    def get_agent_contact_data(self, request, *args, **kwargs):
        contact, cont_exists = Contact.objects.get_or_create(
            user=request.user, contact_type="Агент"
        )
        serializer = self.serializer_class(contact)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def update_agent_contact_data(self, request, *args, **kwargs):
        contact, cont_exists = Contact.objects.get_or_create(
            user=request.user, contact_type="Агент"
        )
        serializer = self.serializer_class(contact, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# noinspection PyMethodMayBeStatic,DuplicatedCode
@extend_schema(tags=["user_profile"])
class UserSubscriptionViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSubscriptionSerializer

    @action(detail=False)
    def get_subscription_data(self, request):
        subscription, subs_exists = Subscription.objects.get_or_create(
            user=request.user
        )
        serializer = self.serializer_class(subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def activate_subscription(self, request):
        user_id = request.data.get("user")
        token = request.data.get("token")
        is_passed = request.data.get("is_passed")

        user = get_object_or_404(User, pk=user_id)
        subscription, subs_exists = Subscription.objects.get_or_create(user=user)
        serializer = self.serializer_class(subscription)

        if token == "111" and is_passed:
            subscription.expiration = datetime.datetime.now(
                tz=UTC
            ) + datetime.timedelta(30)
            subscription.is_active = True
            subscription.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


# region OTHER_STAFF
# noinspection PyMethodMayBeStatic,DuplicatedCode
@extend_schema(tags=["notary"])
class NotaryViewSet(ModelViewSet):
    queryset = Notary.objects.all()
    serializer_class = NotarySerializer
    parser_classes = [MultiPartParser]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


@extend_schema(tags=["service_center"])
class ServiceCenterViewSet(ModelViewSet):
    queryset = ServiceCenter.objects.all()
    serializer_class = ServiceCenterSerializer
    parser_classes = [MultiPartParser]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
# endregion OTHER_STAFF


@extend_schema(tags=["filters"])
class FilterViewSet(ModelViewSet):
    queryset = Filter.objects.all()
    # serializer_class = FilterSerializer
    permission_classes = [IsFilterOwner]
