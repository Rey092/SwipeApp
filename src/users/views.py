from django.contrib.auth import get_user_model

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate(".envs/firebase-auth.json")
firebase_app = firebase_admin.initialize_app(cred)

User = get_user_model()


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
