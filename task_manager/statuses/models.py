from django.db import models
from django.utils.translation import gettext_lazy as _


class TaskStatus(models.Model):
    """Модель статуса задачи"""
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name=_('Имя')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Статус задачи')
        verbose_name_plural = _('Статусы задач')
        ordering = ['-created_at']
