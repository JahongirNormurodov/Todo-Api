from rest_framework import serializers
from .models import Label


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ["id", "name", "color", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class LabelShortSerializer(serializers.ModelSerializer):
    """Todo ichida ishlatiladi — faqat id, name, color"""
    class Meta:
        model = Label
        fields = ["id", "name", "color"]