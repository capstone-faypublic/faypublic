from django.forms import Form, ModelForm
from .models import Project, ProjectSubmission
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class SmallProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['users', 'description']
        widgets = {
        	'expected_completion_date' : DateInput(),
        }

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['users']
        widgets = {
        	'expected_completion_date' : DateInput(),
        }

class ProjectSubmissionForm(ModelForm):
    class Meta:
        model = ProjectSubmission
        exclude = ['project', 'status', 'admin_notes', 'scheduled_time']