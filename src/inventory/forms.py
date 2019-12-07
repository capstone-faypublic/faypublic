from django.forms import Form, ModelForm
from .models import EquipmentCheckout
from django import forms
import arrow
from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class EquipmentCheckoutForm(ModelForm):
    class Meta:
        model = EquipmentCheckout
        exclude = ['user', 'equipment', 'checkout_status', 'due_date']
        widgets = {
            'checkout_date' : DateInput(),
        }
