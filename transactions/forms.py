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

