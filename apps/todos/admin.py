from django.contrib import admin
from .models import Todo, SubTodo


class SubTodoInline(admin.TabularInline):
    model = SubTodo
    extra = 0
    fields = ['title', 'is_completed', 'position']


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'folder', 'priority', 'status', 'due_date', 'created_at']
    list_filter = ['status', 'priority', 'user', 'folder']
    search_fields = ['title', 'description']
    filter_horizontal = ['tags', 'labels']
    inlines = [SubTodoInline]
    ordering = ['-created_at']


@admin.register(SubTodo)
class SubTodoAdmin(admin.ModelAdmin):
    list_display = ['title', 'todo', 'is_completed', 'position']
    list_filter = ['is_completed']
    search_fields = ['title']
