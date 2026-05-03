from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from .models import Todo, SubTodo
from .serializers import TodoListSerializer, TodoDetailSerializer, SubTodoSerializer
from .filters import TodoFilter


@extend_schema(tags=['Todos'])
class TodoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filterset_class = TodoFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'due_date', 'priority', 'position', 'status']
    ordering = ['position', '-created_at']

    def get_queryset(self):
        return (
            Todo.objects
            .filter(user=self.request.user)
            .select_related('folder', 'category')
            .prefetch_related('tags', 'labels', 'sub_todos')
        )

    def get_serializer_class(self):
        if self.action in ('retrieve', 'create', 'update', 'partial_update'):
            return TodoDetailSerializer
        return TodoListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=['Sub-Todos'])
class SubTodoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubTodoSerializer

    def get_queryset(self):
        return SubTodo.objects.filter(
            todo__user=self.request.user,
            todo_id=self.kwargs['todo_pk']
        )

    def perform_create(self, serializer):
        todo = Todo.objects.get(pk=self.kwargs['todo_pk'], user=self.request.user)
        serializer.save(todo=todo)
