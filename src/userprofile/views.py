from django.shortcuts import render

# Create your views here.

def register_producer_user(request):

    # if create account run this to set user group
    # from django.contrib.auth.models import Group
    # group = Group.objects.get(name='groupname')
    # user.groups.add(group)

    return render(
        request,
        'register_producer_user.html',
        context={
        }
    )