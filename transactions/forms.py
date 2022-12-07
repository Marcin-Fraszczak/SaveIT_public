from django import forms
from . import models


class CategoryForm(forms.ModelForm):

    class Meta:
        model = models.Category
        fields = ("name", "description")


class CounterpartyForm(forms.ModelForm):

    class Meta:
        model = models.Counterparty
        fields = ("name", "description")


class WalletForm(forms.ModelForm):

    class Meta:
        model = models.Wallet
        fields = ("name", "description")


class TransactionForm(forms.ModelForm):
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    # value = forms.FloatField(widget=forms.widgets.NumberInput(attrs={'size': 2}))

    class Meta:
        model = models.Transaction
        fields = ("date", "value", "is_profit", "notes", "category", "counterparty", "wallet")





