from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Folder
from .serializers import FolderSerializer
from apps.Todos.models import Todo


class FolderViewSet(viewsets.ModelViewSet):
    """
    GET    /folders/        — barcha folderlar (unpaginated)
    POST   /folders/        — yangi folder yaratish
    GET    /folders/{id}/   — folder detail
    PUT    /folders/{id}/   — to'liq yangilash
    PATCH  /folders/{id}/   — qisman yangilash
    DELETE /folders/{id}/   — o'chirish (cascade todos)
    """
    serializer_class = FolderSerializer
    pagination_class = None  # unpaginated

    def get_queryset(self):
        return Folder.objects.filter(user=self.request.user).order_by("position", "created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FolderTodoViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    GET /folders/{folder_pk}/todos/        — folder ichidagi todolar (paginated)
    GET /folders/{folder_pk}/todos/{id}/   — todo detail
    """
    serializer_class = FolderSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["due_date", "priority", "status", "position", "created_at"]
    ordering = ["position"]

    def get_queryset(self):
        return (
            Todo.objects.filter(
                folder_id=self.kwargs["folder_pk"],
                user=self.request.user
            )
            .select_related("folder")
        )