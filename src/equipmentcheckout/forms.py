from django.forms import Form, ModelForm
from .models import EquipmentCheckout

class EquipmentCheckoutForm(ModelForm):
    class Meta:
        model = EquipmentCheckout
        exclude = ['user']
