from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from userprofile.models import UserProfile

from .models import EquipmentCheckout
from .forms import EquipmentCheckoutForm


# Create your views here.

def equipment(request):
    return render(
        request,
        'equipment.html',
        context={
        }
    )



@login_required
def equipment_checkout(request):
    # user = request.user
    # equipmentcheckout = get_object_or_404(EquipmentCheckout, user=user)
    userprofile = get_object_or_404(UserProfile, user=request.user)

    checkout_form = EquipmentCheckoutForm(request.POST)

    if checkout_form.is_valid():
        equipmentcheckout = checkout_form.save()

    # checkout_form = EquipmentCheckoutForm(instance=equipmentcheckout)

    return render(
        request,
        'checkout.html',
        context={
            'userprofile': userprofile,
            'checkout_form': checkout_form
        }
    )
