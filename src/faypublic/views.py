from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

def home(request):
    return render(
        request,
        'home.html',
        context={
            'somevar': 'this is a context var'
        }
    )

def user_register(request):
    form = UserRegistrationForm(request.POST)

    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        raw_pass = form.cleaned_data.get('password1')
        user = authenticate(
            username=username,
            password=raw_pass
        )
        login(request, user)
        return redirect('user_profile')

    return render(
        request,
        'user_register.html',
        context={
            'form': form
        }
    )

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