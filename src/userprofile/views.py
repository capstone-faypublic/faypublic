from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import UserProfile
from .forms import UserProfileForm
from equipmentcheckout.models import EquipmentCheckout

# Create your views here.
@login_required
def user_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)

    profile_form = UserProfileForm(request.POST, instance=userprofile)

    if profile_form.is_valid():
        userprofile = profile_form.save()

    return render(
        request,
        'profile.html',
        context={
            'name': request.user.first_name + ' ' + request.user.last_name,
            'profile_form': UserProfileForm(instance=userprofile)
        }
    )

@login_required
def user_checkouts(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    checkouts = EquipmentCheckout.objects.filter(user=request.user)
    return render(
        request,
        'user_checkouts.html',
        context={
            'checkouts': checkouts
        }
    )