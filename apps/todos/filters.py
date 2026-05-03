import django_filters
from .models import Todo


class TodoFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Todo.Status.choices)
    priority = django_filters.ChoiceFilter(choices=Todo.Priority.choices)
    category = django_filters.UUIDFilter(field_name='category__id')
    folder = django_filters.UUIDFilter(field_name='folder__id')
    tags = django_filters.BaseInFilter(field_name='tags__id', lookup_expr='in')
    labels = django_filters.BaseInFilter(field_name='labels__id', lookup_expr='in')
    due_date_before = django_filters.DateTimeFilter(field_name='due_date', lookup_expr='lte')
    due_date_after = django_filters.DateTimeFilter(field_name='due_date', lookup_expr='gte')
    is_overdue = django_filters.BooleanFilter(method='filter_overdue')

    class Meta:
        model = Todo
        fields = ['status', 'priority', 'category', 'folder', 'tags', 'labels']

    def filter_overdue(self, queryset, name, value):
        from django.utils import timezone
        if value:
            return queryset.filter(due_date__lt=timezone.now(), status__in=['pending', 'in_progress'])
        return queryset
