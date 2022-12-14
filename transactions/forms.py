from django import forms
from . import models


class TransactionForm(forms.ModelForm):
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = models.Transaction
        fields = ("date", "value", "is_profit", "description", "category", "counterparty", "wallet")

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False
