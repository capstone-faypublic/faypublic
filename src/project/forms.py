from django.forms import Form, ModelForm
from .models import Project, ProjectUpload

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['users']

class ProjectUploadForm(ModelForm):
    class Meta:
        model = ProjectUpload
        exclude = ['project']