from django.forms import Form, ModelForm
from .models import Project, ProjectSubmission

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['users']

class ProjectSubmissionForm(ModelForm):
    class Meta:
        model = ProjectSubmission
        exclude = ['project']