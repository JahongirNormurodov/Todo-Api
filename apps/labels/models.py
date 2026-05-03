from django.conf import settings
from django.db import models
from apps.models import TimeStampedModel


class Label(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='labels'
    )
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#EF4444')

    class Meta:
        ordering = ['name']
        unique_together = ['user', 'name']

    def __str__(self):
        return self.name
