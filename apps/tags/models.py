from django.conf import settings
from django.db import models
from apps.models import TimeStampedModel


class Tag(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tags'
    )
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']
        unique_together = ['user', 'name']

    def __str__(self):
        return f'#{self.name}'

    @property
    def todo_count(self):
        return self.todos.count()
