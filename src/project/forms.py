from django.forms import Form, ModelForm
from .models import Project, ProjectSubmission

class SmallProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['users', 'description']

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['users']

class ProjectSubmissionForm(ModelForm):
    class Meta:
        model = ProjectSubmission
        exclude = ['project', 'status', 'admin_notes', 'scheduled_time']