from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectUpload
from .forms import ProjectForm, ProjectUploadForm
from userprofile.models import UserProfile

# Create your views here.
@login_required
def projects(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)

    project_form = ProjectForm(request.POST)

    if project_form.is_valid():
        project =  project_form.save()
        userprofile.project_set.add(project)

    return render(
        request,
        'projects.html',
        context={
            'userprofile': userprofile,
            'project_form': ProjectForm(),
        }
    )


@login_required
def project(request, id):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    project = get_object_or_404(userprofile.project_set, id=id)

    projectupload_form = ProjectUploadForm(request.POST, request.FILES)

    if projectupload_form.is_valid():
        upload = projectupload_form.save(commit=False)
        upload.project = project
        upload.save()

    return render(
        request,
        'project.html',
        context={
            'project': project,
            'projectupload_form': ProjectUploadForm()
        }
    )