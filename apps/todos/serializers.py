from rest_framework import serializers
from apps.tags.serializers import TagSerializer
from apps.labels.serializers import LabelSerializer
from .models import Todo, SubTodo


class SubTodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTodo
        fields = ['id', 'todo', 'title', 'is_completed', 'position', 'created_at', 'updated_at']
        read_only_fields = ['id', 'todo', 'created_at', 'updated_at']


class TodoListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list endpoints — includes sub_todos."""
    tags = TagSerializer(many=True, read_only=True)
    labels = LabelSerializer(many=True, read_only=True)
    sub_todos = SubTodoSerializer(many=True, read_only=True)
    sub_todo_stats = serializers.ReadOnlyField()

    # Write-only fields for M2M
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True,
        queryset=__import__('apps.tags.models', fromlist=['Tag']).Tag.objects.all(),
        source='tags', required=False
    )
    label_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True,
        queryset=__import__('apps.labels.models', fromlist=['Label']).Label.objects.all(),
        source='labels', required=False
    )

    class Meta:
        model = Todo
        fields = [
            'id', 'folder', 'category',
            'title', 'description', 'priority', 'status',
            'due_date', 'position',
            'tags', 'tag_ids',
            'labels', 'label_ids',
            'sub_todos', 'sub_todo_stats',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TodoDetailSerializer(TodoListSerializer):
    """Full nested detail: folder and category objects expanded."""
    from apps.folders.serializers import FolderSerializer
    from apps.categories.serializers import CategorySerializer

    folder_detail = serializers.SerializerMethodField()
    category_detail = serializers.SerializerMethodField()

    class Meta(TodoListSerializer.Meta):
        fields = TodoListSerializer.Meta.fields + ['folder_detail', 'category_detail']

    def get_folder_detail(self, obj):
        from apps.folders.serializers import FolderSerializer
        return FolderSerializer(obj.folder).data

    def get_category_detail(self, obj):
        from apps.categories.serializers import CategorySerializer
        if obj.category:
            return CategorySerializer(obj.category).data
        return None
