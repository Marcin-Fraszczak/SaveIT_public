from django import forms
from django.contrib.auth import get_user_model

from . import models


class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ("name", "description")

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False


class CounterpartyForm(forms.ModelForm):
    class Meta:
        model = models.Counterparty
        fields = ("name", "description")

    def __init__(self, *args, **kwargs):
        super(CounterpartyForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False


class WalletForm(forms.ModelForm):
    class Meta:
        model = models.Wallet
        fields = ("name", "description")

    def __init__(self, *args, **kwargs):
        super(WalletForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False


class TransactionForm(forms.ModelForm):
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = models.Transaction
        fields = ("date", "value", "is_profit", "description", "category", "counterparty", "wallet")

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False


class SavingsPlanForm(forms.ModelForm):
    class Meta:
        model = models.SavingsPlan
        fields = ("name", "monthly_goal", "initial_value", "curve_type")
