from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, update_session_auth_hash
from .models import UserProfile
from .forms import UserProfileForm
from inventory.models import EquipmentCheckout
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from project.forms import ProgramRequestForm

# Create your views here.

@login_required
def user_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    return render(
        request,
        'profile.html',
        context={
            'profile': userprofile,
        }
    )


@login_required
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    profile_form = UserProfileForm(instance=userprofile)

    if request.POST:
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)

    if profile_form.is_valid():
        userprofile = profile_form.save(commit=False)
        user_get_email_reminders = request.POST.get('user_get_email_reminders')
        userprofile.get_email_reminders = True if user_get_email_reminders == 'on' else False
        user_get_sms_reminders = request.POST.get('user_get_sms_reminders')
        userprofile.get_sms_reminders = True if user_get_sms_reminders == 'on' else False
        userprofile.save()

        user_first_name = request.POST.get('user_first_name')
        user_last_name = request.POST.get('user_last_name')
        user_email = request.POST.get('user_email')
        request.user.first_name = user_first_name
        request.user.last_name = user_last_name
        request.user.email = user_email
        request.user.save()

    return render(
        request,
        'edit_profile.html',
        context={
            'name': request.user.first_name + ' ' + request.user.last_name,
            'profile': userprofile,
            'profile_form': profile_form
        }
    )

@login_required
def user_checkouts(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    checkouts = EquipmentCheckout.objects.filter(user=request.user).order_by('-due_date', '-checkout_date')
    return render(
        request,
        'user_checkouts.html',
        context={
            'checkouts': checkouts
        }
    )


@login_required
def user_classes(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    class_registrations = request.user.classregistration_set.all().order_by('-class_section__date')
    return render(
        request,
        'user_classes.html',
        context={
            'class_registrations': class_registrations
        }
    )


@login_required
def user_change_password(request):
    form = PasswordChangeForm(user=request.user, data=request.POST or None)

    if form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)
        return redirect('/profile/')

    return render(
        request,
        'user_change_password.html',
        context={
            'form': form
        }
    )


@login_required
def user_program_requests(request):
    form = ProgramRequestForm(request.POST)
    program_requests = request.user.programrequest_set.all()

    if form.is_valid():
        req = form.save(commit=False)
        req.user = request.user
        req.save()

    return render(
        request,
        'user_program_requests.html',
        context={
            'form': form,
            'program_requests': program_requests
        }
    )