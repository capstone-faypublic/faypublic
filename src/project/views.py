from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm, SmallProjectForm, ProjectInviteUserForm, ProjectProgramRequestForm
from userprofile.models import UserProfile
from django.contrib.auth.models import User
from django.core.mail import send_mail

# Create your views here.
@login_required
def projects(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)

    project_form = SmallProjectForm(request.POST)

    if project_form.is_valid():
        project =  project_form.save(commit=False)
        project.owner = request.user
        project.save()

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
    project = get_object_or_404(Project, id=id)

    if not project in userprofile.projects():
        return redirect('/profile/projects/')

    invite_user_form = ProjectInviteUserForm(request.POST)
    if request.method == 'POST' and invite_user_form.is_valid():
        email = invite_user_form.cleaned_data['invited_user_email']

        if email != request.user.email:
            invited_user = get_object_or_404(User, email=email)
            project.users.add(invited_user)

    program_request = ProjectProgramRequestForm(request.POST)
    if request.method == 'POST' and program_request.is_valid() and project.uploaded_file:
        req = program_request.save(commit=False)
        req.user = request.user
        req.title = project.title
        req.description = project.description
        req.media_link = project.uploaded_file.url
        req.save()

        redirect('/profile/requests/')

    project_form = ProjectForm(request.POST, request.FILES, instance=project)
    if request.method == 'POST' and project_form.is_valid():
        project = project_form.save()

    return render(
        request,
        'project.html',
        context={
            'project': project,
            'project_form': ProjectForm(instance=project),
            'invite_user_form': ProjectInviteUserForm(),
            'project_program_request_form': ProjectProgramRequestForm()
        }
    )


@login_required
def cancel_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if project.owner == request.user:
        project.delete()

    return redirect('user_projects')