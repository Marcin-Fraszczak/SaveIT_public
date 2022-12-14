from django.contrib.auth import get_user_model
from django.db import models


CURVES = (
    (1, "Linear"),
    (2, "Parabolic"),
    (3, "Logarithmic"),
)


class SavingsPlan(models.Model):
    name = models.CharField(max_length=60)
    unique_name = models.CharField(max_length=200)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='savings_plan')
    monthly_goal = models.FloatField()
    initial_value = models.FloatField()
    curve_type = models.IntegerField(choices=CURVES)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name

