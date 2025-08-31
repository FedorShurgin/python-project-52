from django.db import models

from task_manager.labels.models import Label
from task_manager.statuses.models import Status


class Task(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Имя",
    )
    description = models.TextField(
        verbose_name="Описание"
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name="Статус",
        null=True,
    )
    author = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='created_task',
        null=True,
    )
    executor = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='executor_task',
        verbose_name="Исполнитель",
        null=True,
    )
    labels = models.ManyToManyField(
        Label,
        related_name='tasks',
        verbose_name="Метки",
    )
    date_create = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.name
