from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from userprofile.models import UserProfile
from django.db.models import Q
from .models import Equipment, EquipmentCategory, EquipmentCheckout
from .forms import EquipmentCheckoutForm
import arrow
from .models import RESERVED
from project.models import Project



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
    if timeframe == "CHECKOUT_24HR":
        now = arrow.get(checkout_date)
        due = now.shift(days=2).date()
        return due
    if timeframe == "CHECKOUT_WEEK":
        now = arrow.get(checkout_date)
        due = now.shift(days=6).date()
        return due
    else:
        return "5555-05-05"

@login_required
def equipment_checkout(request, slug):
    equipment = get_object_or_404(Equipment, slug=slug)
    userprofile = get_object_or_404(UserProfile, user=request.user)

    checkout_form = EquipmentCheckoutForm(request.POST)

    if checkout_form.is_valid():
        project_id = request.POST.get('project_id')
        project = get_object_or_404(Project, id=project_id)

        if userprofile.can_checkout_equipment(equipment):
            checkout = checkout_form.save(commit=False)
            checkout.equipment = equipment
            checkout.user = request.user
            checkout.due_date = compute_due_date(checkout.equipment.checkout_timeframe, checkout.checkout_date)
            checkout.project = project
            checkout.checkout_status = RESERVED
            checkout.save()

            return redirect('user_checkouts')

    return render(
        request,
        'equipment_checkout.html',
        context={
            'equipment': equipment,
            'userprofile': userprofile,
            'checkout_form': checkout_form
        }
    )
