from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import UserProfile
from .forms import UserProfileForm

# Create your views here.
@login_required
def user_profile(request):
    user = request.user
    userprofile = get_object_or_404(UserProfile, user=user)
    profile_form = UserProfileForm(instance=userprofile)

    if profile_form.is_valid():
        profile_form.save()

    return render(
        request,
        'profile.html',
        context={
            'name': user.first_name + ' ' + user.last_name,
            'profile_form': profile_form
        }
    ) 