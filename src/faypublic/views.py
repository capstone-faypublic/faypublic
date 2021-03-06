import arrow
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from userprofile.models import UserProfile
from inventory.models import EquipmentCheckout
from classes.models import ClassSection
from .tasks import send_equipment_pickup_reminder, send_equipment_due_reminder, send_equipment_overdue_notification, send_class_registration_reminder

def home(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        checkouts = EquipmentCheckout.objects.filter(user=request.user).order_by('-due_date', '-checkout_date')
        class_registrations = request.user.classregistration_set.all().order_by('-class_section__date')

        userprofile = get_object_or_404(UserProfile, user=request.user)

        return render(
            request,
            'home.html',
            context={
                'checkouts': checkouts,
                'class_registrations': class_registrations,
                'profile': userprofile,
            }
        )
    elif request.user.is_authenticated:
        today = arrow.get(timezone.now())
        today_start = today.floor('day').datetime
        today_end = today.ceil('day').datetime

        overdue_checkouts = EquipmentCheckout.objects.filter(
            due_date__lte=today_end,
            checkout_status='CHECKED_OUT'
        ).order_by('-due_date', '-checkout_date')

        todays_classes = ClassSection.objects.filter(
            date__gte=today_start,
            date__lte=today_end
        )
        return render(
            request,
            'admin_home.html',
            context={
                'overdue_checkouts': overdue_checkouts,
                'todays_classes': todays_classes
            }
        )
    else:
        return render(
            request,
            'home_login.html',
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