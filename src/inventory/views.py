from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.admin.views.decorators import staff_member_required
from userprofile.models import UserProfile
from django.db.models import Q
from .models import Equipment, EquipmentCategory, EquipmentCheckout, ClosedDay
from .forms import EquipmentCheckoutForm
import arrow
from .models import RESERVED, CHECKED_OUT
from project.models import Project
from django.http import JsonResponse
import dateutil


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
def equipment_checkout(request, slug):
    equipment = get_object_or_404(Equipment, slug=slug)

    checkout_form = EquipmentCheckoutForm(request.POST or None)

    err_msg = ''

    userprofile = None
    try:
        userprofile = UserProfile.objects.get(user=request.user)
    except:
        userprofile = None

    if checkout_form.is_valid():
        userprofile = get_object_or_404(UserProfile, user=request.user)
        project_id = request.POST.get('project')
        checkout_time = int(request.POST.get('checkout_time')) if request.POST.get('checkout_time') else 0
        project = get_object_or_404(Project, id=project_id)

        if userprofile.can_checkout_equipment(equipment):
            checkout = checkout_form.save(commit=False)

            checkout.equipment = equipment
            checkout.user = request.user

            # checkouts starting
            if not checkout.equipment.checkout_timeframe == 'CHECKOUT_3HR':
                checkout.checkout_date = arrow.get(checkout.checkout_date).replace(hour=10).datetime
            else:
                checkout.checkout_date = arrow.get(checkout.checkout_date).replace(hour=checkout_time).datetime


            checkout.due_date = compute_due_date(checkout.equipment.checkout_timeframe, checkout.checkout_date)
            checkout.project = project
            checkout.checkout_status = RESERVED

            if not closed_on_day(checkout.checkout_date):
                units = available_units(equipment, checkout.checkout_date, checkout.due_date)

                if units > 0:
                    if not user_has_current_checkout(request.user, equipment):
                        checkout.save()

                        return redirect('user_checkouts')
                    else:
                        err_msg = 'Sorry, you currently have this item checked out'
                else:
                    err_msg = 'Sorry, there are no units available for that date'
            else:
                err_msg = 'Sorry, we are closed that day!'
        else:
            err_msg = 'Sorry, you haven\'t completed the prerequisites necessary to check out this item'

    return render(
        request,
        'equipment_checkout.html',
        context={
            'equipment': equipment,
            'userprofile': userprofile,
            'checkout_form': checkout_form,
            'err_msg': err_msg
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