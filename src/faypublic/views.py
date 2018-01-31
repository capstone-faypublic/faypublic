from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm

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

def user_login(request):
    form = AuthenticationForm(request.POST)

    val = [0]

    if form.is_valid():
        val.append(1)
        username = form.cleaned_data.get('username')
        raw_pass = form.cleaned_data.get('password')

        user = authenticate(
            username=username,
            password=raw_pass
        )
        login(request, user)
        return redirect('user_profile')

    val.append(2)
    return render(
        request,
        'user_login.html',
        context={
            'form': form,
            'val': val
        }
    )

def user_logout(request):
    logout() 

def user_profile(request):
    return render(
        request,
        'home.html',
    ) 