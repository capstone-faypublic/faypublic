from django.forms import Form, ModelForm
from .models import EquipmentCheckout
from project.models import Project
from django import forms
import arrow
from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class EquipmentCheckoutForm(ModelForm):
    class Meta:
        model = EquipmentCheckout
        exclude = ['user', 'checkout_status', 'due_date']
        widgets = {
            'checkout_date' : DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        initial = kwargs.get('initial')
        user = initial.get('user') or None

        if user and not user.is_superuser:
            self.fields['project'].choices = Project.objects.filter(users=user)
        else:
            self.fields['project'].choices = []