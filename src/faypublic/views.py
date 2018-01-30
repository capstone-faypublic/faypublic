from django.shortcuts import render
from django.contrib.auth import login, authenticate

def home(request):
    return render(
        request,
        'home.html',
        context={
            'somevar': 'this is a context var'
        }
    )

def user_register(request):
    return render(
        request,
        'user_register.html',
        context={
        }
    )

def user_login(request):
    return render(
        request,
        'user_register.html',
        context={
        }
    )

def user_logout(request):
    logout() 