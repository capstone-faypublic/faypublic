from django.forms import Form, ModelForm
from .models import UserProfile
from django import forms
from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user', 'badges', 'get_sms_reminders', 'get_email_reminders', 'proof_of_residency']
        widgets = {
        	'birthdate': DateInput(),
        }