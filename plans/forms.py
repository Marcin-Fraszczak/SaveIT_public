from django import forms
from . import models


class SavingsPlanForm(forms.ModelForm):
    class Meta:
        model = models.SavingsPlan
        fields = ("name", "monthly_goal", "initial_value", "curve_type")
