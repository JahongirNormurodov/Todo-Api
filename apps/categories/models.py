from django.conf import settings
from django.db import models
from apps.models import TimeStampedModel


class Category(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories'
    )
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#10B981')
    icon = models.CharField(max_length=50, default='tag')

    class Meta:
        ordering = ['name']
        unique_together = ['user', 'name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return f'{self.user.email} / {self.name}'
