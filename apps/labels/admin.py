from django.contrib import admin
from .models import Label


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'color', 'created_at']
    list_filter = ['user']
    search_fields = ['name']
