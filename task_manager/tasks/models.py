from django.db import models
from django.conf import settings
from task_manager.labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    description = models.TextField(blank=True, verbose_name="Описание")
    status = models.ForeignKey(
        "statuses.Status",
        on_delete=models.PROTECT,
        verbose_name="Статус"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_tasks"
    )
    executor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="assigned_tasks",
        verbose_name="Исполнитель"
    )
    labels = models.ManyToManyField(Label, blank=True, verbose_name="Метки")

    def __str__(self):
        return self.name
