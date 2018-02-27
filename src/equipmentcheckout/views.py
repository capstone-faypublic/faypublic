from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from userprofile.models import UserProfile
from django.db.models import Q
from .models import Equipment, EquipmentCategory, EquipmentCheckout
from .forms import EquipmentCheckoutForm
import arrow


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
    if val == "CHECKOUT_24hr":
        now = arrow.utcnow()
        due = now.replace(hour=+24)
        return due
    if val == "CHECKOUT_WEEK":
        now = arrow.utcnow()
        due = now.replace(hour=+120)
        return due

@login_required
def equipment_checkout(request, slug):
    # user = request.user
    # equipmentcheckout = get_object_or_404(EquipmentCheckout, user=user)
    item = get_object_or_404(Equipment, slug=slug)
    userprofile = get_object_or_404(UserProfile, user=request.user)

    checkout_form = EquipmentCheckoutForm(request.POST, initial={'due_date':'2018-02-28'})
    checkout_form.fields["due_date"].initial = arrow.utcnow()

    new_due_date = compute_due_date(item.checkout_timeframe)

    if checkout_form.is_valid():
        equipmentcheckout = checkout_form.save(commit=False)
        # equipmentcheckout.due_date = '2018-02-28'
        equipmentcheckout.save()

    # checkout_form = EquipmentCheckoutForm(instance=equipmentcheckout)

    return render(
        request,
        'equipment_checkout.html',
        context={
            'item': item,
            'userprofile': userprofile,
            'checkout_form': checkout_form
        }
    )
