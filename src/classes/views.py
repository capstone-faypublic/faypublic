from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render
from .models import Class
from django.http import HttpResponse

# Create your views here.


@login_required
def class_registration(request, slug):
    course = get_object_or_404(Class, slug=slug)
    return render(
        request,
        'class_registration.html',
        context={
            'class': course
        }
    )


def class_list(request):
    classes = Class.objects.order_by("id")[:]
    return render(
        request, 
        'class_list.html', 
        context={
            "classes" : classes
        }
    )



