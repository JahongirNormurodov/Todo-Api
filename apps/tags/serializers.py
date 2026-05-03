from rest_framework import serializers
from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    todo_count = serializers.ReadOnlyField()

    class Meta:
        model = Tag
        fields = ['id', 'name', 'todo_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
