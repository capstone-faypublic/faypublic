from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render
from .models import Course
from django.http import HttpResponse

# Create your views here.
# @login_required
# def course_listing(request):
#     courseList = Course.objects.order_by("id")[:]
#     output = ", ".join([c.course_title for c in courseList])
#     return HttpResponse("You're looking at question./n" + output )


def course_listing(request):
    courseList = Course.objects.order_by("id")[:]
    output = ", ".join([c.course_title for c in courseList])
    return render(request, 'course.html', context={"output" : courseList})



