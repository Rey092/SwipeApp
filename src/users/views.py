from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model
from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet

from src.users.models import Message
from src.users.serializers import MessageSerializer, MessageRecipientUserSerializer

User = get_user_model()


# noinspection PyMethodMayBeStatic
@extend_schema(tags=["messages"])
class MessageList(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        """Returns a list of all Users that received messages or sent them to current User."""

        queryset = User.objects.prefetch_related("received_messages", "sent_messages"). \
            filter(Q(received_messages__sender=request.user) | Q(sent_messages__recipient=request.user))
        serializer = MessageRecipientUserSerializer(queryset, many=True)
        return Response({'result': 'success', 'data': serializer.data})

    def create(self, request):
        """Create a new message where sender is current User and recipient is target User."""

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save(sender=request.user)
            return Response({'result': 'success', 'data': serializer.data})
        else:
            return Response({'result': serializer.errors}, status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        """Returns a list of all Messages between current User and target User."""

        queryset = Message.objects.select_related("sender", "recipient") \
            .filter(Q(sender=request.user, recipient__pk=pk) | Q(sender__pk=pk, recipient=request.user)) \
            .order_by('-created')
        serializer = self.serializer_class(queryset, many=True)
        return Response({'result': 'success', 'data': serializer.data})
