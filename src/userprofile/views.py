from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import UserProfile

# Create your views here.
@login_required
def user_profile(request):
    user = request.user

    return render(
        request,
        'profile.html',
        context={
            'name': user.first_name + ' ' + user.last_name
        }
    ) 