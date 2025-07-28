from django.contrib.auth.models import User
from django.db import models

from task_manager.labels.models import LabelsModel
from task_manager.statuses.models import StatusesModel


class TasksModel(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Имя",
    )
    description = models.TextField(
        verbose_name="Описание"
    )
    status = models.ForeignKey(
        StatusesModel,
        on_delete=models.PROTECT,
        verbose_name="Статус",
        null=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='created_task',
        null=True,
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='executor_task',
        verbose_name="Исполнитель",
        null=True,
    )
    labels = models.ManyToManyField(
        LabelsModel,
        related_name='tasks',
        verbose_name="Метки",
    )
    date_create = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.name
