from django import forms
from . import models


class WalletForm(forms.ModelForm):
    class Meta:
        model = models.Wallet
        fields = ("name", "description")

    def __init__(self, *args, **kwargs):
        super(WalletForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False
