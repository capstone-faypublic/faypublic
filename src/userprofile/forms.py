from django.forms import Form, ModelForm
from .models import UserProfile
from django import forms

class DateInput(forms.DateInput):
	input_type = 'date'

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']
        widgets = {
        	'birthdate' : DateInput(),
        }