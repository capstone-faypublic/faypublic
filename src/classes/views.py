from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render
from .models import Class, ClassSection, ClassRegistration
from django.http import HttpResponse
import arrow
from django.db.models import Q
from userprofile.models import UserProfile

# Create your views here.


def user_registered_for_class_section(section, user):
    for reg in section.classregistration_set.all():
        if user == reg.user:
            return True
    return False


@login_required
def class_registration(request, slug):
    course = get_object_or_404(Class, slug=slug)

    err_msg = ''

    if request.method == 'POST':
        section_id = request.POST.get('section_id')
        class_section = get_object_or_404(ClassSection, id=section_id, date__gte=arrow.utcnow().datetime)

        userprofile = get_object_or_404(UserProfile, user=request.user)

        if(class_section.number_open_seats() > 0):
            # check to make sure a user isn't already registered, it's really easy to reload the page and re-register for a course

            if userprofile.can_register_for_class(class_section.class_key):
                if not user_registered_for_class_section(class_section, request.user):
                    reg = ClassRegistration(
                        user=request.user,
                        class_section=class_section,
                    )
                    reg.save()

                    return redirect('user_classes')

                else:
                    err_msg = 'You are already registered for this section'
            else:
                err_msg = 'You have not met the prerequisites to take this class'
        else:
            err_msg = 'This class section is full'

    return render(
        request,
        'class_registration.html',
        context={
            'class': course,
            'err_msg': err_msg
        }
    )


def class_list(request):
    classes = Class.objects.all()

    search = ''
    if request.GET.get('q') and len(request.GET['q']) > 0:
        search = request.GET['q']
        classes = classes.filter(Q(class_title__icontains=search))

    return render(
        request, 
        'class_list.html', 
        context={
            'classes': classes,
            'search': search
        }
    )



