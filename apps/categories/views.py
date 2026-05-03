from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from .models import Category
from .serializers import CategorySerializer


@extend_schema(tags=['Categories'])
class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    pagination_class = None  # Unpaginated

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=['Category Todos'])
class CategoryTodoViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Read-only: todos inside a specific category."""
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        from apps.todos.serializers import TodoListSerializer
        return TodoListSerializer

    def get_queryset(self):
        from apps.todos.models import Todo
        return (
            Todo.objects
            .filter(user=self.request.user, category_id=self.kwargs['category_pk'])
            .select_related('folder', 'category')
            .prefetch_related('tags', 'labels', 'sub_todos')
        )

    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'due_date', 'priority', 'position']
    ordering = ['position']
