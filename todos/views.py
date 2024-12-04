from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Todo
from .serializers import TodoSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.authentication import TokenAuthentication

# Create your views here.

@extend_schema_view(
    list=extend_schema(description='Get list of todos for current user'),
    create=extend_schema(description='Create a new todo'),
    retrieve=extend_schema(
        description='Get a specific todo by ID',
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='A unique integer value identifying this todo'
            ),
        ]
    ),
    update=extend_schema(
        description='Update a todo',
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='A unique integer value identifying this todo'
            ),
        ]
    ),
    partial_update=extend_schema(
        description='Partially update a todo',
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='A unique integer value identifying this todo'
            ),
        ]
    ),
    destroy=extend_schema(
        description='Delete a todo',
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='A unique integer value identifying this todo'
            ),
        ]
    ),
)
class TodoViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Todo items.
    
    Requires token authentication.
    Use the /api-token-auth/ endpoint to obtain a token.
    """
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    lookup_field = 'id'

    def get_queryset(self):
        """
        Return todos for the current authenticated user
        """
        return Todo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Save the todo with the current user
        """
        serializer.save(
            user=self.request.user,
            created_by=self.request.user,
            updated_by=self.request.user
        )

    def perform_update(self, serializer):
        """
        Update the todo with the current user as updater
        """
        serializer.save(updated_by=self.request.user)
