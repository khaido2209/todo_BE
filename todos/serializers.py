from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    """
    Serializer for Todo model with complete CRUD operations
    """
    class Meta:
        model = Todo
        fields = ['id', 'title', 'description', 'completed', 
                 'created_at', 'updated_at', 'created_by', 'updated_by']
        read_only_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
        
        # Add help text for fields
        extra_kwargs = {
            'title': {'help_text': 'Title of the todo item'},
            'description': {'help_text': 'Detailed description of the todo item'},
            'completed': {'help_text': 'Whether the todo item is completed'},
        }