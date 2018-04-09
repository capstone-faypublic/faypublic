from django.forms import Form, ModelForm
from .models import UserProfile
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user', 'badges', 'get_sms_reminders', 'get_email_reminders']
        widgets = {
            'birthdate' : DateInput(),
        }