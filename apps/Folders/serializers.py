from rest_framework import serializers
from .models import Folder

class FolderSerializer(serializers.ModelSerializer):
    todo_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Folder
        fields = '__all__'