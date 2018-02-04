from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import UserProfile
from .forms import UserProfileForm

# Create your views here.
@login_required
def user_profile(request):
    user = request.user
    userprofile = UserProfile.objects.get(user=user)
    profile_form = UserProfileForm(request.POST, instance=userprofile)

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