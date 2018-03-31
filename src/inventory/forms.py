from django.forms import Form, ModelForm
from .models import EquipmentCheckout
from django import forms
import arrow

class DateInput(forms.DateInput):
    input_type = 'date'

class EquipmentCheckoutForm(ModelForm):
    class Meta:
        model = EquipmentCheckout
        exclude = ['user', 'equipment', 'checkout_status', 'due_date', 'project']
        widgets = {
            'checkout_date' : DateInput(),
        }
