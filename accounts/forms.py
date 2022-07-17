from django.forms import ModelForm
from django import forms
from .models import Account
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(ModelForm):
    first_name = forms.CharField(max_length = 100, help_text = 'First Name')
    last_name = forms.CharField(max_length = 100, help_text = 'Last Name')
    email = forms.EmailField(max_length = 150, help_text = 'Email')
    phone_number = forms.CharField(max_length = 11, help_text = 'Phone Number')
    password1 = forms.CharField(max_length = 100, help_text = 'Create password')
    password2 = forms.CharField(max_length = 100, help_text = 'Repeat password')

    class Meta:
        model = Account
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2')