from django.forms import Form, ModelForm
from .models import EquipmentCheckout
from django import forms
import arrow

class DateInput(forms.DateInput):
    input_type = 'date'

class EquipmentCheckoutForm(ModelForm):
    find_out = forms.DateField(
        initial="2018-02-28",
        label='Test Field',
        help_text='For Initial Value Testing'
    )

    class Meta:
        model = EquipmentCheckout
        exclude = ['user']
        widgets = {
            'checkout_date' : DateInput(),
        }
