from django.db import models

# Create your models here.
class StatusesModel(models.Model):
    name = models.CharField(max_length=255)
    date_create = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name