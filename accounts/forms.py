from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={}))

    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ("username", "email", "password1")
        help_texts = {
            'username': None,
        }


class CustomUserChangeForm(UserChangeForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={}))

    class Meta:
        model = get_user_model()
        fields = UserChangeForm.Meta.fields
        fields = ("username", "password1")
