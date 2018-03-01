from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from userprofile.models import UserProfile
from django.db.models import Q
from .models import Equipment, EquipmentCategory, EquipmentCheckout
from .forms import EquipmentCheckoutForm
import arrow
from .models import RESERVED



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


def compute_due_date(val):
    if val == "CHECKOUT_24HR":
        now = arrow.utcnow()
        due = now.shift(days=2).date()
        return due
    if val == "CHECKOUT_WEEK":
        now = arrow.utcnow()
        due = now.shift(days=6).date()
        return due
    else:
        return "2018-03-15"

@login_required
def equipment_checkout(request, slug):
    equipment = get_object_or_404(Equipment, slug=slug)
    userprofile = get_object_or_404(UserProfile, user=request.user)

    checkout_form = EquipmentCheckoutForm(request.POST)

    if checkout_form.is_valid():
        checkout = checkout_form.save(commit=False)
        checkout.equipment = equipment
        checkout.user = request.user
        checkout.due_date = compute_due_date(checkout.equipment.checkout_timeframe)
        checkout.checkout_status = RESERVED
        checkout.save()

    return render(
        request,
        'equipment_checkout.html',
        context={
            'equipment': equipment,
            'userprofile': userprofile,
            'checkout_form': checkout_form
        }
    )
