from django import forms
from django.forms import ModelForm
from .models import Order


class OrderForm(forms.Form):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name','phone', 'email', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'order_note']