from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectSubmission
from .forms import ProjectForm, ProjectSubmissionForm, SmallProjectForm
from userprofile.models import UserProfile

# Create your views here.
@login_required
def projects(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)

    project_form = SmallProjectForm(request.POST)

    if project_form.is_valid():
        project =  project_form.save()
        userprofile.project_set.add(project)

    return render(
        request,
        'projects.html',
        context={
            'userprofile': userprofile,
            'project_form': SmallProjectForm(),
        }
    )


@login_required
def project(request, id):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    project = get_object_or_404(userprofile.project_set, id=id)

    submission_form = ProjectSubmissionForm(request.POST, request.FILES)

    if submission_form.is_valid():
        upload = submission_form.save(commit=False)
        upload.project = project
        upload.save()

    project_form = ProjectForm(request.POST, instance=project)

    if project_form.is_valid():
        project_form.save()

    return render(
        request,
        'project.html',
        context={
            'project': project,
            'project_form': ProjectForm(instance=project),
            'submission_form': ProjectSubmissionForm()
        }
    )