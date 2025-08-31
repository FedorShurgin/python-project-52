from django.db import models


class Label(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    author = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        null=True,
    )
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
