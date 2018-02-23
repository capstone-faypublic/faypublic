from django.forms import Form, ModelForm
from .models import EquipmentCheckout
from django import forms

class DateInput(forms.DateInput):
	input_type = 'date'

class EquipmentCheckoutForm(ModelForm):
    class Meta:
        model = EquipmentCheckout
        exclude = ['user']
        widgets = {
        	'checkout_date' : DateInput(),
        }
