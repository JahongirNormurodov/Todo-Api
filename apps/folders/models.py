from django.conf import settings
from django.db import models
from apps.models import TimeStampedModel


class Folder(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='folders'
    )
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=7, default='#6366F1')  # hex color
    icon = models.CharField(max_length=50, default='folder')
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['position', 'created_at']
        unique_together = ['user', 'name']

    def __str__(self):
        return f'{self.user.email} / {self.name}'

    @property
    def todo_count(self):
        return self.todos.count()
