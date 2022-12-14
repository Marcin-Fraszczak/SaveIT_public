from django import forms
from .models import SavingsPlan


class SavingsPlanForm(forms.ModelForm):
    class Meta:
        model = SavingsPlan
        fields = ("name", "monthly_goal", "initial_value", "curve_type")
