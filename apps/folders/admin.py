from django.contrib import admin
from .models import Folder


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'color', 'position', 'created_at']
    list_filter = ['user']
    search_fields = ['name', 'user__email']
