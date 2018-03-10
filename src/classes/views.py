from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render
from .models import Class
from django.http import HttpResponse

# Create your views here.
# @login_required
# def class_listing(request):
#     classList = Class.objects.order_by("id")[:]
#     output = ", ".join([c.class_title for c in classList])
#     return HttpResponse("You're looking at question./n" + output )


def class_listing(request):
    classList = Class.objects.order_by("id")[:]
    output = ", ".join([c.class_title for c in classList])
    return render(request, 'class.html', context={"output" : classList})



