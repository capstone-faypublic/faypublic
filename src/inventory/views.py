import json
from tkinter import N
from dateutil import tz
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.admin.views.decorators import staff_member_required
from django.forms import modelformset_factory
import userprofile
from userprofile.models import UserProfile
from django.contrib.auth.models import User
from django.db.models import Q
from .models import CHECKOUT_24HR, Equipment, EquipmentCategory, EquipmentCheckout, ClosedDay
from .forms import EquipmentCheckoutForm
import arrow
from .models import RESERVED, CHECKED_OUT
from project.models import Project
from django.http import JsonResponse
import dateutil
from django import forms
from functools import partial
from datetime import datetime
from django.utils.timezone import make_aware
DateInput = partial(forms.DateInput, {'class': 'datepicker'})

# Create your views here.

def equipment_category(request, slug):
    category = get_object_or_404(EquipmentCategory, slug=slug)
    equipment = Equipment.objects.filter(category=category)
    categories = EquipmentCategory.objects.all()

    search = ''
    if request.GET.get('q') and len(request.GET['q']) > 0:
        search = request.GET['q']
        # equipment = Equipment.objects.filter(make__icontains=search)
        equipment = equipment.filter(
            Q(make__icontains=search) | Q(model__icontains=search)
        )

    return render(
        request,
        'equipment_list.html',
        context={
            'search': search,
            'equipment': equipment,
            'categories': categories,
            'category': category
        }
    )

def equipment_list(request):
    equipment = Equipment.objects.all()
    categories = EquipmentCategory.objects.all()

    search = ''
    if request.GET.get('q') and len(request.GET['q']) > 0:
        search = request.GET['q']
        # equipment = Equipment.objects.filter(make__icontains=search)
        equipment = equipment.filter(
            Q(make__icontains=search) | Q(model__icontains=search)
        )

    return render(
        request,
        'equipment_list.html',
        context={
            'search': search,
            'equipment': equipment,
            'categories': categories
        }
    )


def compute_due_date(timeframe, checkout_date):
    if timeframe == 'CHECKOUT_3HR':
        res = arrow.get(checkout_date)
        due = res.shift(hours=3)

        return due.datetime

    elif timeframe == "CHECKOUT_24HR":
        res = arrow.get(checkout_date)
        due = res.shift(days=1).replace(hour=19)

        # mon=0, tues=1, wed=2, thurs=3, fri=4, sat=5, sun=6
        # if due on wed or sun, shift one day
        # this is a naive shift, more handling will be done in the checkout_or_due_date_on_closed_day function
        if due.weekday() == 2 or due.weekday() == 6:
            due = due.shift(days=1)

        return due.datetime

    elif timeframe == "CHECKOUT_WEEK":
        res = arrow.get(checkout_date)

        # always due on a tuesday
        # shift a day to combat reserved-on-tues/due-on-tues
        due = res.shift(days=+1).shift(weekday=1).replace(hour=19)

        return due.datetime
    return None

def closed_on_day(date):
    weekday = arrow.get(date).weekday()
    closed_days = ClosedDay.objects.filter(
        Q(day_of_week=weekday)
        & (
            (Q(begin_date=None) & Q(end_date=None))
            | (Q(begin_date__lte=date) & Q(end_date=None))
            | (Q(begin_date=None) & Q(end_date__gte=date))
            | (Q(begin_date__lte=date) & Q(end_date__gte=date))
        )
    )

    return len(closed_days) > 0

@login_required
def equipment_details(request, slug):
    equipment = get_object_or_404(Equipment, slug=slug)

    return render(
        request,
        'equipment_details.html',
        context={
            'equipment': equipment,
        }
    )


@login_required
def cancel_checkout(request, checkout_id):
    checkout = get_object_or_404(EquipmentCheckout, id=checkout_id)

    if checkout.user == request.user and checkout.checkout_status == 'RESERVED':
        checkout.checkout_status = 'CANCELED'
        checkout.save()

    return redirect('user_checkouts')


def item_checkouts(request, item_id):
    start = request.GET.get('start')
    end = request.GET.get('end')

    start_date = arrow.get(start, 'YYYY-MM-DDThh:mm:ss').datetime
    end_date = arrow.get(end, 'YYYY-MM-DDThh:mm:ss').datetime


    all_checkouts = EquipmentCheckout.objects.filter(
        (Q(checkout_status='RESERVED')
        | Q(checkout_status='CHECKED_OUT'))
        & (Q(checkout_date__gte=start_date)
        | Q(due_date__lte=end_date))
        & Q(equipment__id=item_id)
    )

    checkouts = []
    for checkout in all_checkouts:

        print(checkout.checkout_date)

        # checkout_date = checkout.checkout_date.strftime('%Y-%m-%d %H:%M')
        # due_date = checkout.due_date.strftime('%Y-%m-%d %H:%M')
        checkout_date = arrow.get(checkout.checkout_date).shift(hours=-5).datetime
        due_date = arrow.get(checkout.due_date).shift(hours=-5).datetime
        checkouts.append({
            'equipment_id': checkout.equipment.id,
            'equipment_name': checkout.equipment.name(),
            'checkout_timeframe': checkout.equipment.checkout_timeframe,
            'start': checkout_date,
            'end': due_date,
            'status': checkout.checkout_status,
            'title': checkout.equipment.name(),
            'allDay': False
        })

    return JsonResponse(checkouts, safe=False)


@staff_member_required
def admin_calendar(request):
    return render(
        request,
        'admin_calendar.html',
        context={
        }
    )

@staff_member_required
def admin_events(request):
    start = request.GET.get('start')
    end = request.GET.get('end')

    start_date = arrow.get(start, 'YYYY-MM-DDThh:mm:ss').shift(hours=-5).datetime
    end_date = arrow.get(end, 'YYYY-MM-DDThh:mm:ss').shift(hours=-5).datetime


    all_checkouts = EquipmentCheckout.objects.filter(
        (Q(checkout_status='RESERVED')
        | Q(checkout_status='CHECKED_OUT'))
        & (Q(checkout_date__gte=start_date)
        & Q(due_date__lte=end_date))
    )

    checkouts = []
    for checkout in all_checkouts:

        print(checkout.checkout_date)

        checkout_date = arrow.get(checkout.checkout_date).datetime
        due_date = arrow.get(checkout.due_date).datetime
        checkouts.append({
            'equipment_id': checkout.equipment.id,
            'equipment_name': checkout.equipment.name(),
            'checkout_timeframe': checkout.equipment.checkout_timeframe,
            'start': checkout_date,
            'end': due_date,
            'status': checkout.checkout_status,
            'title': str(checkout.user) + ' - ' + checkout.equipment.name(),
            'allDay': False,
            'displayEventTime': True,
            'displayEventEnd': True
        })

    return JsonResponse(checkouts, safe=False)

def user_has_overdue_checkout(user):
    today = arrow.utcnow().date()
    overdue_checkouts = EquipmentCheckout.objects.filter(
        Q(user=user)
        & Q(checkout_status='CHECKED_OUT')
        & Q(due_date__lte=today)
    )
    return len(overdue_checkouts) > 0

def user_has_required_badges(user, equipment):
    if user.is_superuser:
        return True

    try:
        profile = UserProfile.objects.get(user=user)
        return profile.can_checkout_equipment(equipment)
    except:
        registrations = user.classregistration_set.filter(completed=True)
        badges = []

        for reg in registrations:
            sect = reg.class_section
            course = sect.class_key
            for badge in course.awarded_badges.all():
                badges.append(badge)

        for req in equipment.prerequisite_badges.all():
            if req not in badges:
                return False

        return True

def user_has_current_checkout(user, item):
    today = arrow.utcnow().date()
    checkouts = EquipmentCheckout.objects.filter(
        Q(equipment=item)
        & Q(user=user)
        & (
            Q(checkout_status='RESERVED')
            | Q(checkout_status='CHECKED_OUT')
        )
    )
    return len(checkouts) > 0

def available_units(item, start_date, end_date):
    all_item_checkouts = EquipmentCheckout.objects.filter(equipment=item)
    checked_out_on_date = all_item_checkouts.filter(
        (Q(checkout_date__gte=start_date) & Q(checkout_date__lte=end_date) & Q(due_date__gte=end_date)) # overlaps the checkout_date
        | (Q(checkout_date__lte=start_date) & Q(due_date__gte=start_date) &Q(due_date__lte=end_date)) # overlaps the due_date
        | (Q(checkout_date__lte=start_date) & Q(due_date__gte=end_date)) # within checkout_date and due_date
        | (Q(checkout_date__gte=start_date) & Q(due_date__lte=end_date)) # wraps checkout_date and due_date
    )
    checked_out_by_status = checked_out_on_date.filter(Q(checkout_status=RESERVED) | Q(checkout_status=CHECKED_OUT))

    return item.quantity - len(checked_out_by_status)

@csrf_exempt
@staff_member_required
def get_user_projects_json(request):
    data = json.loads(request.body)

    if data.get('user_id'):
        user = None
        try:
            user = User.objects.get(id=data.get('user_id'))
        except:
            return JsonResponse({ 'error': 'User does not exist' }, status=404)

        # the user has no overdue checkouts
        if user_has_overdue_checkout(user):
            return JsonResponse({ 'error': 'User has overdue checkouts' }, status=400)

        projects = []
        for p in user.owner_projects.all():
            projects.append({ 'id': p.id, 'title': p.title })
        for p in user.project_set.all():
            projects.append({ 'id': p.id, 'title': p.title })

        return JsonResponse({ 'projects': projects }, status=200)

    return JsonResponse({ 'error': 'Invalid request' }, status=400)

@csrf_exempt
@login_required
def check_user_can_check_out_equipment(request):
    data = json.loads(request.body)

    if data.get('equipment_id') and data.get('checkout_start_date'):
        user = None
        if request.user.is_superuser and data.get('user_id'):
            try:
                user = User.objects.get(id=data.get('user_id'))
            except:
                return JsonResponse({ 'error': 'User does not exist' }, status=404)
        elif request.user.is_superuser:
            return JsonResponse({ 'error': 'User not selected' }, status=400)
        else:
            user = request.user

        equipment = None
        equipment_id = data.get('equipment_id')

        if not equipment_id:
            return JsonResponse({ 'error': 'Invalid selection' }, status=400)

        try:
            equipment = Equipment.objects.get(id=equipment_id)
        except:
            return JsonResponse({ 'error': 'Invalid selection' }, status=400)


        # there are available units
        checkout_date = make_aware(datetime.strptime(data.get('checkout_start_date'), '%Y-%m-%d'))
        due_date = compute_due_date(equipment.checkout_timeframe, checkout_date)
        if not available_units(equipment, checkout_date, due_date):
            return JsonResponse({ 'error': 'No units available for selected checkout date' }, status=400)

        # the user does not currently have the item checked out
        if user_has_current_checkout(user, equipment):
            return JsonResponse({ 'error': 'User has item checked out' }, status=400)

        # the user has the prerequisite classes/badges
        if not user_has_required_badges(user, equipment):
            return JsonResponse({ 'error': 'User does not have prerequisite badges' }, status=400)

        return JsonResponse({ 'valid': True }, status=200)

    return JsonResponse({ 'error': 'Invalid request, equipment and checkout date required' }, status=400)

@csrf_exempt
@login_required
def handle_equipment_checkout_form(request):
    data = json.loads(request.body)

    checkout_start_date = data.get('checkout_start_date') 
    checkout_time = int(data.get('checkout_time'))
    project_id = int(data.get('project_id'))
    equipment_ids = data.get('equipment_ids')
    user = None

    if not checkout_start_date or not checkout_time or not equipment_ids or len(equipment_ids) is 0:
        return JsonResponse({ 'error': 'Invalid submission', 'checkout_start_date': checkout_start_date, 'checkout_time': checkout_time, 'equipment_ids': equipment_ids }, status=400)

    if request.user.is_superuser:
        user_id = data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except:
            return JsonResponse({ 'error': 'User does not exist' }, status=404)
    else:
        user = request.user

    # re-validate checkout details for each item then save

    # the user has no overdue checkouts
    if user_has_overdue_checkout(user):
        return JsonResponse({ 'error': 'User has overdue checkouts' }, status=400)

    global_checkout_timeframe = CHECKOUT_24HR if len(equipment_ids) > 1 else None

    checkouts = []
    errors = {}
    has_errors = False

    for equipment_id in equipment_ids:
        equipment = None
        equipment_errors = []

        try:
            equipment = Equipment.objects.get(id=int(equipment_id))
        except:
            equipment_errors.append('Equipment does not exist')

        checkout_date = arrow.get(checkout_start_date).replace(hour=checkout_time, tzinfo='US/Central').datetime
        due_date = compute_due_date(global_checkout_timeframe if global_checkout_timeframe else equipment.checkout_timeframe, checkout_date)

        if closed_on_day(checkout_date):
            equipment_errors.append('We are closed that day')

        if not available_units(equipment, checkout_date, due_date):
            equipment_errors.append('No units available for selected checkout date')

        # the user does not currently have the item checked out
        if user_has_current_checkout(user, equipment):
            equipment_errors.append('User has item checked out')

        # the user has the prerequisite classes/badges
        if not user_has_required_badges(user, equipment):
            equipment_errors.append('User does not have required badges')

        project = None

        try:
            project = Project.objects.get(id=project_id)
        except:
            equipment_errors.append('Project does not exist')

        if len(equipment_errors) > 0:
            errors[equipment_id] = equipment_errors
            has_errors = True
            break

        checkout = EquipmentCheckout.objects.create(
            user=user,
            equipment=equipment,
            project=project,
            checkout_date=checkout_date,
            due_date=due_date
        )

        checkouts.append({
            'equipment_id': checkout.equipment.id,
            'equipment_name': checkout.equipment.name(),
            'checkout_timeframe': checkout.equipment.checkout_timeframe,
            'start': checkout_date,
            'end': due_date,
            'status': checkout.checkout_status,
            'title': str(checkout.user) + ' - ' + checkout.equipment.name()
        })


    if has_errors:
        return JsonResponse({ 'errors': errors, 'checkouts': checkouts }, status=400)

    return JsonResponse({ 'checkouts': checkouts }, safe=False, status=200)

@login_required
def checkout_page(request):
    users = None
    user_projects = None
    equipment_list = Equipment.objects.all()

    if request.user.is_superuser:
        users = User.objects.all()
    else:
        profile = UserProfile.objects.get(user=request.user)
        user_projects = profile.projects()

    return render(
        request,
        'checkout_page.html',
        context={
            'users': users,
            'user_projects': user_projects,
            'equipment_list': equipment_list,
        }
    )