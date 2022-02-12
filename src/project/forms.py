from django.forms import Form, ModelForm
from .models import Project, ProgramRequest
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
        exclude = ['owner', 'users', 'uploaded_file']
        widgets = {
        	'expected_completion_date' : DateInput(),
        }



def validate_user_exists(user_email):
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        raise ValidationError('User does not exist')


class ProjectInviteUserForm(Form):
    invited_user_email = forms.EmailField(
        label='Invite user',
        required=True,
        validators=[validate_user_exists]
    )


class ProjectProgramRequestForm(ModelForm):
    class Meta:
        model = ProgramRequest
        exclude = ['user', 'title', 'description', 'requested_on', 'media_link', 'status']
        widgets = {
            'requested_play_date': DateInput()
        }

class ProgramRequestForm(ModelForm):
    class Meta:
        model = ProgramRequest
        exclude = ['user', 'requested_on', 'status']
        widgets = {
            'requested_play_date': DateInput()
        }