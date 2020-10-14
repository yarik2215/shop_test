from django import forms
from django.forms import fields
from django.utils.translation import gettext_lazy as _
from .models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'comment']

class AddToCartForm(forms.Form):
    quantity = forms.fields.IntegerField(min_value=1, max_value=999, label=_('Quantity'), initial=1)

