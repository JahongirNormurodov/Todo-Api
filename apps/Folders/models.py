import uuid
from django.db import models
 
 
class Folder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=7, default="#6366F1")
    icon = models.CharField(max_length=50, blank=True, default="")
    position = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        ordering = ["position", "created_at"]
 
    def __str__(self):
        return self.name
 
    @property
    def todo_count(self):
        return self.todos.count()
