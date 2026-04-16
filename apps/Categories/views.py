from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category
from .serializers import CategorySerializer
from apps.todos.serializers import TodoListSerializer
from apps.todos.filters import TodoFilter
from apps.todos.models import Todo


class CategoryViewSet(viewsets.ModelViewSet):
    """
    GET    /categories/        — barcha kategoriyalar (unpaginated)
    POST   /categories/        — yangi kategoriya yaratish
    GET    /categories/{id}/   — kategoriya detail
    PUT    /categories/{id}/   — to'liq yangilash
    PATCH  /categories/{id}/   — qisman yangilash
    DELETE /categories/{id}/   — o'chirish
    """
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    pagination_class = None  # unpaginated


class CategoryTodoViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    GET /categories/{category_pk}/todos/        — category ichidagi todolar (paginated)
    GET /categories/{category_pk}/todos/{id}/   — todo detail
    """
    serializer_class = TodoListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TodoFilter
    search_fields = ["title", "description"]
    ordering_fields = ["due_date", "priority", "status", "position", "created_at"]
    ordering = ["position"]

    def get_queryset(self):
        return (
            Todo.objects.filter(category_id=self.kwargs["category_pk"])
            .select_related("folder", "category")
            .prefetch_related("tags", "labels", "sub_todos")
        )
