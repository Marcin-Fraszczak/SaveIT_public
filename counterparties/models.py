from django.contrib.auth import get_user_model
from django.db import models


class Counterparty(models.Model):
    name = models.CharField(max_length=60)
    unique_name = models.CharField(max_length=200)
    description = models.CharField(max_length=80, default="", null=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='own_counterparty')

    def __str__(self):
        return self.name
