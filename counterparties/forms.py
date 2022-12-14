from django import forms
from .models import Counterparty


class CounterpartyForm(forms.ModelForm):
    class Meta:
        model = Counterparty
        fields = ("name", "description")

    def __init__(self, *args, **kwargs):
        super(CounterpartyForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False
