from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import Course
from django.http import HttpResponse

# Create your views here.
# @login_required
def course_listing(request):

    return HttpResponse("You're looking at question.")


