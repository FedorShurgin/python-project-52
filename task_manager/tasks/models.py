from django.db import models
from django.contrib.auth.models import User
from task_manager.statuses.models import StatusesModel
from task_manager.labels.models import LabelsModel

# Create your models here.
class TasksModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.ForeignKey(StatusesModel, on_delete=models.PROTECT, null=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_task', null=True)
    executor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='executor_task', null=True)
    labels = models.ManyToManyField(LabelsModel)
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
