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



