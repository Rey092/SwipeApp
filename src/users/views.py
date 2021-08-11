from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from src.users.serializers import UploadSerializer


User = get_user_model()


# noinspection PyMethodMayBeStatic
@extend_schema(tags=["messages"])
class UploadViewSet(ViewSet):
    serializer_class = UploadSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        file_uploaded = request.FILES.get('file_uploaded')
        content_type = file_uploaded.content_type
        response = "POST API and you have uploaded a {} file".format(content_type)
        return Response(response)


# @extend_schema
# class HelloViewSet(ViewSet):
#     """Test API ViewSet"""
#     serializer_class = HelloSerializer
#
#     def list(self, request):
#         """Return a Hello message"""
#
#         view_set = [
#             'Uses actions (list, create, retrieve, update, partial_update)',
#             'Automatically maps to URLs using Routers',
#             'Provides more functionality with less code',
#         ]
#
#         return Response({'message': 'Hello', 'view_set': view_set})
#
#     def create(self, request):
#         """Create a new hello message"""
#         serializer = self.serializer_class(data=request.data)
#
#         if serializer.is_valid():
#             name = serializer.validated_data.get('name')
#             message = f'Hello {name}!'
#             return Response({'message': message})
#         else:
#             return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
#
#     def retrieve(self, request, pk=None):
#         """Handle getting an object by its ID"""
#         return Response({'http_method': 'GET'})
#
#     def update(self, request, pk=None):
#         """Handle updating an object"""
#         return Response({'http_method': 'PUT'})
#
#     def partial_update(self, request, pk=None):
#         """Handle updating part of an object"""
#         return Response({'http_method': 'PATCH'})
#
#     def destroy(self, request, pk=None):
#         """Handle removing an object"""
#         return Response({'http_method': 'DELETE'})
