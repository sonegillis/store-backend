from django import forms

from landing.models import Order
from landing.widgets import CartItemWidget


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        widgets = {
            'cart': CartItemWidget()
        }
        fields = '__all__'


