from rest_framework import serializers
from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    todo_count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ["id", "name", "todo_count", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_todo_count(self, obj):
        return obj.todo_count


class TagShortSerializer(serializers.ModelSerializer):
    """Todo ichida ishlatiladi — faqat id va name"""
    class Meta:
        model = Tag
        fields = ["id", "name"]