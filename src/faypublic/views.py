from django.shortcuts import render

def home(request):
    return render(
        request,
        'home.html',
        context={
            'somevar': 'this is a context var'
        }
    )