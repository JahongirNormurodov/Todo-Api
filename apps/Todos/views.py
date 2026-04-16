from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Todo, SubTodo
from .serializers import (
    TodoListSerializer,
    TodoDetailSerializer,
    TodoWriteSerializer,
    SubTodoSerializer,
)


class TodoViewSet(viewsets.ModelViewSet):
    """
    GET    /todos/        — todolar ro'yxati (paginated, sub_todos bilan)
    POST   /todos/        — yangi todo yaratish
    GET    /todos/{id}/   — todo detail (nested folder, category, sub_todos)
    PUT    /todos/{id}/   — to'liq yangilash
    PATCH  /todos/{id}/   — qisman yangilash
    DELETE /todos/{id}/   — o'chirish (cascade sub_todos)
    """
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["due_date", "priority", "status", "position", "created_at"]
    ordering = ["position"]

    def get_queryset(self):
        return (
            Todo.objects.filter(user=self.request.user)
            .select_related("folder")
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TodoDetailSerializer
        if self.action in ("create", "update", "partial_update"):
            return TodoWriteSerializer
        return TodoListSerializer


class SubTodoViewSet(viewsets.ModelViewSet):
    """
    GET    /todos/{todo_pk}/sub-todos/        — sub-todolar ro'yxati
    POST   /todos/{todo_pk}/sub-todos/        — yangi sub-todo yaratish
    GET    /todos/{todo_pk}/sub-todos/{id}/   — sub-todo detail
    PUT    /todos/{todo_pk}/sub-todos/{id}/   — to'liq yangilash
    PATCH  /todos/{todo_pk}/sub-todos/{id}/   — qisman yangilash (toggle)
    DELETE /todos/{todo_pk}/sub-todos/{id}/   — o'chirish
    """
    serializer_class = SubTodoSerializer
    pagination_class = None

    def get_queryset(self):
        return SubTodo.objects.filter(
            todo_id=self.kwargs["todo_pk"]
        ).order_by("position", "created_at")

    def perform_create(self, serializer):
        serializer.save(todo_id=self.kwargs["todo_pk"])


