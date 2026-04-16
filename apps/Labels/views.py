from rest_framework import viewsets
from .models import Label
from .serializers import LabelSerializer


class LabelViewSet(viewsets.ModelViewSet):
    """
    GET    /labels/        — barcha labellar (unpaginated)
    POST   /labels/        — yangi label yaratish
    GET    /labels/{id}/   — label detail
    PUT    /labels/{id}/   — to'liq yangilash
    PATCH  /labels/{id}/   — qisman yangilash
    DELETE /labels/{id}/   — o'chirish
    """
    queryset = Label.objects.all().order_by("name")
    serializer_class = LabelSerializer
    pagination_class = None  # unpaginated