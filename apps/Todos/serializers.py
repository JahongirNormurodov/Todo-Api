from rest_framework import serializers
from .models import Todo, SubTodo
from apps.Folders.serializers import FolderSerializer


class SubTodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTodo
        fields = "__all__"


class TodoListSerializer(serializers.ModelSerializer):
    """
    GET /todos/ va nested /folders/.../todos/ uchun.
    sub_todos to'liq array ko'rinishda qaytadi.
    """
    sub_todos = SubTodoSerializer(many=True, read_only=True)
    sub_todo_stats = serializers.SerializerMethodField()

    class Meta:
        model = Todo
        fields = "__all__"
        

    def get_sub_todo_stats(self, obj):
        sub_todos = obj.sub_todos.all()
        return {
            "total": sub_todos.count(),
            "completed": sub_todos.filter(is_completed=True).count(),
        }


class TodoDetailSerializer(serializers.ModelSerializer):
    """
    GET /todos/{id}/ — folder nested ko'rinishda.
    """
    folder = FolderSerializer(read_only=True)
    sub_todos = SubTodoSerializer(many=True, read_only=True)
    sub_todo_stats = serializers.SerializerMethodField()

    class Meta:
        model = Todo
        fields = "__all__"

    def get_sub_todo_stats(self, obj):
        sub_todos = obj.sub_todos.all()
        return {
            "total": sub_todos.count(),
            "completed": sub_todos.filter(is_completed=True).count(),
        }


class TodoWriteSerializer(serializers.ModelSerializer):
    """
    POST, PUT, PATCH /todos/ uchun.
    """

    class Meta:
        model = Todo
        fields = "__all__"

    def create(self, validated_data):
        tags = validated_data.pop("tags", [])
        labels = validated_data.pop("labels", [])
        todo = Todo.objects.create(**validated_data)
        todo.tags.set(tags)
        todo.labels.set(labels)
        return todo

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        labels = validated_data.pop("labels", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tags is not None:
            instance.tags.set(tags)
        if labels is not None:
            instance.labels.set(labels)
        return instance

##
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'
        read_only_fields = ['user']