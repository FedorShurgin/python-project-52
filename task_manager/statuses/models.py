from django.db import models
from django.contrib.auth.models import User


class StatusesModel(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
