from django.forms import ModelForm
from django import forms
from .models import Account
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(ModelForm):

    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput())
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password', 'confirm_password']