from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from userprofile.models import UserProfile
from .tasks import send_equipment_pickup_reminder, send_equipment_due_reminder, send_equipment_overdue_notification, send_class_registration_reminder

def home(request):
    return render(
        request,
        'home.html',
        context={
        }
    )

def user_register(request):
    form = UserRegistrationForm(request.POST or None)

    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        raw_pass = form.cleaned_data.get('password1')
        user = authenticate(
            username=username,
            password=raw_pass
        )
        login(request, user)
        userprofile = UserProfile.objects.create(
            user=user
        )
        userprofile.save()

        if request.GET.get('next'):
            requested_page = request.GET['next']
            return redirect(requested_page)

        return redirect('edit_profile')

    return render(
        request,
        'user_register.html',
        context={
            'form': form
        }
    )

def test_notifications(request):
    send_equipment_pickup_reminder()
    send_equipment_due_reminder()
    send_equipment_overdue_notification()
    send_class_registration_reminder()
    return redirect('/')