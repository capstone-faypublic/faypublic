from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectSubmission
from .forms import ProjectForm, ProjectSubmissionForm, SmallProjectForm, ProjectInviteUserForm
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

    if not project.owner == request.user and not project in request.user.project_set.all():
        return redirect('/profile/projects/')

    submission_form = ProjectSubmissionForm(request.POST, request.FILES)
    if submission_form.is_valid():
        upload = submission_form.save(commit=False)
        upload.project = project
        upload.save()

    invite_user_form = ProjectInviteUserForm(request.POST)
    if invite_user_form.is_valid():
        email = invite_user_form.cleaned_data['invited_user_email']

        if email != request.user.email:
            invited_user = get_object_or_404(User, email=email)
            project.users.add(invited_user)

    project_form = ProjectForm(request.POST, instance=project)
    if project_form.is_valid():
        project_form.save()

    return render(
        request,
        'project.html',
        context={
            'project': project,
            'project_form': ProjectForm(instance=project),
            'submission_form': ProjectSubmissionForm(),
            'invite_user_form': ProjectInviteUserForm()
        }
    )