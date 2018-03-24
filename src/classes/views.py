from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render
from .models import Class, ClassSection, ClassRegistration
from django.http import HttpResponse
import arrow

# Create your views here.


@login_required
def class_registration(request, slug):
    course = get_object_or_404(Class, slug=slug)

    if request.method == 'POST':
        section_id = request.POST.get('section_id')
        class_section = get_object_or_404(ClassSection, id=section_id, date__gte=arrow.utcnow().datetime)

        if(class_section.number_open_seats() > 0):
            # check to make sure a user isn't already registered, it's really easy to reload the page and re-register for a course
            reg = ClassRegistration(
                user=request.user,
                class_section=class_section,
            )
            reg.save()
            # redirect to the profile and class registration list

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



