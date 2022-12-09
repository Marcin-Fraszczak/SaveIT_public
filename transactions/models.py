from django.contrib.auth import get_user_model
from django.db import models

CURVES = (
    (1, "Linear"),
    (2, "Exponential"),
    (3, "Logarithmic"),
)


class Transaction(models.Model):
    date = models.DateField()
    value = models.FloatField()
    is_profit = models.BooleanField(default=False)
    notes = models.CharField(max_length=100, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='cat_transaction')
    counterparty = models.ForeignKey('Counterparty', on_delete=models.CASCADE, related_name='ctr_transaction')
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='own_transaction')
    wallet = models.ManyToManyField('Wallet', related_name='wlt_transaction')

    def __str__(self):
        name = f"{self.date} {self.value} {self.counterparty}"
        return name


class Category(models.Model):
    name = models.CharField(max_length=60)
    unique_name = models.CharField(max_length=200)
    description = models.CharField(max_length=80, null=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='own_category')

    def __str__(self):
        return self.name



class Counterparty(models.Model):
    name = models.CharField(max_length=60)
    unique_name = models.CharField(max_length=200)
    description = models.CharField(max_length=80, null=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='own_counterparty')

    def __str__(self):
        return self.name


class Wallet(models.Model):
    name = models.CharField(max_length=60)
    unique_name = models.CharField(max_length=200)
    description = models.CharField(max_length=80, null=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='wallet')

    def __str__(self):
        return self.name


class SavingsPlan(models.Model):
    name = models.CharField(max_length=60)
    unique_name = models.CharField(max_length=200)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='savings_plan')
    monthly_goal = models.FloatField()
    initial_value = models.FloatField()
    curve_type = models.IntegerField(choices=CURVES)

    def __str__(self):
        return self.name
