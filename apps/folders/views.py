from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from .models import Folder
from .serializers import FolderSerializer


@extend_schema(tags=['Folders'])
class FolderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FolderSerializer
    pagination_class = None  # Folders are unpaginated

    def get_queryset(self):
        return Folder.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=['Folder Todos'])
class FolderTodoViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Read-only: todos inside a specific folder."""
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        from apps.todos.serializers import TodoListSerializer
        return TodoListSerializer

    def get_queryset(self):
        from apps.todos.models import Todo
        return (
            Todo.objects
            .filter(user=self.request.user, folder_id=self.kwargs['folder_pk'])
            .select_related('folder', 'category')
            .prefetch_related('tags', 'labels', 'sub_todos')
        )

    def get_filterset_class(self):
        from apps.todos.filters import TodoFilter
        return TodoFilter

    filterset_fields = []
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'due_date', 'priority', 'position']
    ordering = ['position']
