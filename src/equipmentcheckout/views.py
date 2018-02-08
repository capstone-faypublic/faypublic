from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
# from .models import UserProfile
# from .forms import UserProfileForm

from .models import EquipmentCheckout
from .forms import EquipmentCheckoutForm


# Create your views here.
@login_required
def equipment_checkout(request):
    user = request.user
    userprofile = get_object_or_404(UserProfile, user=user)

    profile_form = UserProfileForm(request.POST, instance=userprofile)

    if profile_form.is_valid():
        userprofile = profile_form.save()

    profile_form = UserProfileForm(instance=userprofile)

    return render(
        request,
        'checkout.html',
        context={
            'name': user.first_name + ' ' + user.last_name,
            'checkout_form': checkout_form
        }
    )
