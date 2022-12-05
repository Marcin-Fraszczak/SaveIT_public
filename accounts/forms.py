from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={}))

    class Meta(UserCreationForm):
        model = get_user_model()
        # fields = UserCreationForm.Meta.fields
        fields = ("username", "email", "password1")
        help_texts = {
            'username': None,
            # 'password': None,
            # 'password1': None,
            # 'password2': None,
            # WTF 3 linie
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = UserChangeForm.Meta.fields
