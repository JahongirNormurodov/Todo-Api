from django.db import models
import uuid
from apps.Folders.models import Folder

class Todo(models.Model):
    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        URGENT = "urgent", "Urgent"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    folder = models.ForeignKey(
        Folder, on_delete=models.CASCADE, related_name="todos"
    )
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, default="")
    priority = models.CharField(
        max_length=10, choices=Priority.choices, default=Priority.MEDIUM
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    due_date = models.DateTimeField(null=True, blank=True)
    position = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["position", "-created_at"]

    def __str__(self):
        return self.title


class SubTodo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    todo = models.ForeignKey(
        Todo, on_delete=models.CASCADE, related_name="sub_todos"
    )
    title = models.CharField(max_length=500)
    is_completed = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["position", "created_at"]

    def __str__(self):
        return f"{self.todo.title} → {self.title}"


