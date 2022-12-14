from django.contrib.auth import get_user_model
from django.db import models


class Transaction(models.Model):
    date = models.DateField()
    value = models.FloatField()
    is_profit = models.BooleanField(default=False)
    description = models.CharField(max_length=100, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='cat_transaction')
    counterparty = models.ForeignKey('Counterparty', on_delete=models.CASCADE, related_name='ctr_transaction')
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='own_transaction')
    wallet = models.ManyToManyField('Wallet', related_name='wlt_transaction')

    def __str__(self):
        name = f"{self.date} {self.value} {self.counterparty}"
        return name
