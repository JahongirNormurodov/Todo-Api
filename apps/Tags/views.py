from rest_framework import viewsets
from .models import Tag
from .serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    """
    GET    /tags/        — barcha taglar (unpaginated)
    POST   /tags/        — yangi tag yaratish
    GET    /tags/{id}/   — tag detail
    PUT    /tags/{id}/   — to'liq yangilash
    PATCH  /tags/{id}/   — qisman yangilash
    DELETE /tags/{id}/   — o'chirish
    """
    queryset = Tag.objects.all().order_by("name")
    serializer_class = TagSerializer
    pagination_class = None  # unpaginated
