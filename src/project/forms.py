from django.forms import Form, ModelForm
from .models import Project
from django import forms
from functools import partial
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class SmallProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['owner', 'users', 'description']
        widgets = {
        	'expected_completion_date' : DateInput(),
        }

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['owner', 'users']
        widgets = {
        	'expected_completion_date' : DateInput(),
        }



def validate_user_exists(user_email):
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        raise ValidationError('User does not exist')


class ProjectInviteUserForm(Form):
    # project_id = forms.IntegerField(
    #     required=True,
    #     validators=[validate_project_exists]
    # )
    invited_user_email = forms.EmailField(
        label='Invite user',
        required=True,
        validators=[validate_user_exists]
    )