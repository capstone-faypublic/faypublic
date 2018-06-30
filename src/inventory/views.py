from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.admin.views.decorators import staff_member_required
from userprofile.models import UserProfile
from django.db.models import Q
from .models import Equipment, EquipmentCategory, EquipmentCheckout
from .forms import EquipmentCheckoutForm
import arrow
from .models import RESERVED
from project.models import Project
from django.http import JsonResponse


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
        due = res.shift(days=1).replace(hour=17)

        # mon=0, tues=1, wed=2, thurs=3, fri=4, sat=5, sun=6
        # if due on wed or sun, shift one day
        if due.weekday() == 2 or due.weekday() == 6:
            due = due.shift(days=1)

        return due.datetime

    elif timeframe == "CHECKOUT_WEEK":
        res = arrow.get(checkout_date)

        # always due on a tuesday
        # shift a day to combat reserved-on-tues/due-on-tues
        due = res.shift(day=1).shift(weekday=1).replace(hour=17)

        return due.datetime
    return None



def available_units(item, start_date, end_date):
    checkouts = EquipmentCheckout.objects.filter(
        Q(equipment=item)
        & (
            Q(checkout_date__gte=start_date)
            & Q(due_date__lte=end_date)
        )
        & (
            Q(checkout_status='RESERVED')
            | Q(checkout_status='CHECKED_OUT')
        )
    )
    return item.quantity - len(checkouts)

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


@login_required
def equipment_checkout(request, slug):
    equipment = get_object_or_404(Equipment, slug=slug)

    checkout_form = EquipmentCheckoutForm(request.POST)

    err_msg = ''

    userprofile = None
    try:
        userprofile = UserProfile.objects.get(user=request.user)
    except:
        userprofile = None

    if checkout_form.is_valid():
        userprofile = get_object_or_404(UserProfile, user=request.user)
        project_id = request.POST.get('project_id')
        checkout_time = int(request.POST.get('checkout_time')) if request.POST.get('checkout_time') else 0
        project = get_object_or_404(Project, id=project_id)

        if userprofile.can_checkout_equipment(equipment):
            checkout = checkout_form.save(commit=False)
            checkout_date = checkout.checkout_date
            due_date = compute_due_date(
                equipment.checkout_timeframe, checkout.checkout_date
            )

            if available_units(equipment, checkout_date, due_date) > 0:
                if not user_has_current_checkout(request.user, equipment):
                    checkout.equipment = equipment
                    checkout.user = request.user

                    # checkouts starting
                    if not checkout.equipment.checkout_timeframe == 'CHECKOUT_3HR':
                        checkout.checkout_date = arrow.get(checkout.checkout_date).replace(hour=10).datetime
                    else:
                        checkout.checkout_date = arrow.get(checkout_date).replace(hour=checkout_time).datetime


                    checkout.due_date = compute_due_date(checkout.equipment.checkout_timeframe, checkout.checkout_date)
                    checkout.project = project
                    checkout.checkout_status = RESERVED
                    checkout.save()

                    return redirect('user_checkouts')
                else:
                    err_msg = 'Sorry, you currently have this item checked out'
            else:
                err_msg = 'Sorry, there are units available for that date'
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

    print(start_date)
    print(end_date)


    all_checkouts = EquipmentCheckout.objects.filter(
        (Q(checkout_status='RESERVED')
        | Q(checkout_status='CHECKED_OUT'))
        & (Q(checkout_date__gte=start_date)
        | Q(due_date__lte=end_date))
        & Q(equipment__id=item_id)
    )

    print(len(all_checkouts))

    checkouts = []
    for checkout in all_checkouts:

        checkout_date = checkout.checkout_date.strftime('%Y-%m-%d')
        due_date = checkout.due_date.strftime('%Y-%m-%d')
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

    start_date = arrow.get(start, 'YYYY-MM-DDThh:mm:ss').datetime
    end_date = arrow.get(end, 'YYYY-MM-DDThh:mm:ss').datetime


    all_checkouts = EquipmentCheckout.objects.filter(
        (Q(checkout_status='RESERVED')
        | Q(checkout_status='CHECKED_OUT'))
        & (Q(checkout_date__gte=start_date)
        & Q(due_date__lte=end_date))
    )

    checkouts = []
    for checkout in all_checkouts:

        checkout_date = checkout.checkout_date.strftime('%Y-%m-%d %H:%M')
        due_date = checkout.due_date.strftime('%Y-%m-%d %H:%M')
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