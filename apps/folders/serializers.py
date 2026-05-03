from rest_framework import serializers
from .models import Folder


class FolderSerializer(serializers.ModelSerializer):
    todo_count = serializers.ReadOnlyField()

    class Meta:
        model = Folder
        fields = ['id', 'name', 'color', 'icon', 'position', 'todo_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
