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

    class Meta:
        model = models.Transaction
        fields = ("date", "value", "is_profit", "notes", "category", "counterparty", "wallet")


class SavingsPlanForm(forms.ModelForm):
    class Meta:
        model = models.SavingsPlan
        fields = ("name", "wallet", "monthly_goal", "initial_value", "curve_type")


