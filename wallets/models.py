from django.contrib.auth import get_user_model
from django.db import models


class Wallet(models.Model):
    name = models.CharField(max_length=60)
    unique_name = models.CharField(max_length=200)
    description = models.CharField(max_length=80, null=True)
    is_default = models.BooleanField(default=False)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='wallet')

    def __str__(self):
        return self.name

