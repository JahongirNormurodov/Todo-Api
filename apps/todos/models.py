from django.conf import settings
from django.db import models
from apps.models import TimeStampedModel


class Todo(TimeStampedModel):
    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='todos'
    )
    folder = models.ForeignKey(
        'folders.Folder',
        on_delete=models.CASCADE,
        related_name='todos'
    )
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.SET_NULL,
        related_name='todos',
        null=True,
        blank=True
    )
    tags = models.ManyToManyField(
        'tags.Tag',
        related_name='todos',
        blank=True
    )
    labels = models.ManyToManyField(
        'labels.Label',
        related_name='todos',
        blank=True
    )

    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    due_date = models.DateTimeField(null=True, blank=True)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['position', '-created_at']

    def __str__(self):
        return self.title

    @property
    def sub_todo_stats(self):
        sub_todos = self.sub_todos.all()
        total = len(sub_todos)
        completed = sum(1 for s in sub_todos if s.is_completed)
        return {'total': total, 'completed': completed}


class SubTodo(TimeStampedModel):
    todo = models.ForeignKey(
        Todo,
        on_delete=models.CASCADE,
        related_name='sub_todos'
    )
    title = models.CharField(max_length=500)
    is_completed = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['position', 'created_at']

    def __str__(self):
        return f'{self.todo.title} → {self.title}'
