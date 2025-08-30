from django.contrib.auth.models import AbstractUser


class CustomModelUsers(AbstractUser):
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"