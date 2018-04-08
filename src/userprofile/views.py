from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, update_session_auth_hash
from .models import UserProfile
from .forms import UserProfileForm
from inventory.models import EquipmentCheckout
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm

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
    profile_form = UserProfileForm(request.POST, instance=userprofile)

    if profile_form.is_valid():
        userprofile = profile_form.save()
        user_first_name = request.POST.get('user_first_name')
        user_last_name = request.POST.get('user_last_name')
        request.user.first_name = user_first_name
        request.user.last_name = user_last_name
        request.user.save()

    return render(
        request,
        'edit_profile.html',
        context={
            'name': request.user.first_name + ' ' + request.user.last_name,
            'profile_form': UserProfileForm(instance=userprofile)
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