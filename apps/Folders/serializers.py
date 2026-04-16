from rest_framework import serializers
from .models import Folder
 
 
class FolderSerializer(serializers.ModelSerializer):
    todo_count = serializers.SerializerMethodField()
 
    class Meta:
        model = Folder
        fields = "__all__"
        
    def get_todo_count(self, obj):
        return obj.todo_count