import django_filters
from .models import Todo


class TodoFilter(django_filters.FilterSet):
    tags = django_filters.BaseInFilter(field_name="tags__id", lookup_expr="in")
    labels = django_filters.BaseInFilter(field_name="labels__id", lookup_expr="in")
    due_date_before = django_filters.DateTimeFilter(field_name="due_date", lookup_expr="lte")
    due_date_after = django_filters.DateTimeFilter(field_name="due_date", lookup_expr="gte")

    class Meta:
        model = Todo
        fields = {
            "status": ["exact"],
            "priority": ["exact"],
            "category": ["exact"],
            "folder": ["exact"],
        }