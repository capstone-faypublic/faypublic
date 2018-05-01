import arrow, datetime
from django.shortcuts import render
from .forms import ReportDateRangeForm
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q

from classes.models import Class, ClassSection, ClassRegistration
from inventory.models import Equipment, EquipmentCategory, EquipmentCheckout
from project.models import Project, ProgramRequest
from userprofile.models import UserProfile, Badge


def get_classes_data(start_date, end_date):
    classes = Class.objects.order_by('class_title')

    classes_data = []

    for c in classes:
        sections = c.classsection_set.all().filter(
            Q(date__gte=start_date)
            & Q(date__lte=end_date)
        )

        data = {
            'title': c.class_title,
            'sections': []
        }

        for s in sections:
            registered = s.classregistration_set.all()

            sect_data = {
                'date': s.date,
                'seats_available': s.seats_available,
                'registered': registered.count(),
                'completed': registered.filter(completed=True).count(),
                'incomplete': registered.filter(completed=False).count()
            }

            data['sections'].append(sect_data)

        classes_data.append(data)

    return classes_data



def get_inventory_data(start_date, end_date):
    categories = EquipmentCategory.objects.order_by('title')

    inventory_data = []

    for c in categories:
        equipment = c.equipment_set.order_by('make', 'model')

        data = {
            'category': c.title,
            'equipment': []
        }

        for e in equipment:
            checkouts = e.equipmentcheckout_set.all().filter(
                Q(checkout_date__gte=start_date)
                & Q(checkout_date__lte=end_date)
            )

            equipment_data = {
                'name': e.name(),
                'checkouts': checkouts.count()
            }
            data['equipment'].append(equipment_data)
        
        inventory_data.append(data)

    return inventory_data


def get_project_data(start_date, end_date):
    projects = Project.objects.order_by('title')
    equipment = Equipment.objects.order_by('make', 'model')

    project_data = {
        'projects': [],
        'equipment': [e.name() for e in equipment]
    }

    for p in projects:
        checkouts = []
        for e in equipment:
            num = p.equipmentcheckout_set.all().filter(
                Q(equipment=e)
                & Q(checkout_date__gte=start_date)
                & Q(checkout_date__lte=end_date)
            ).count()
            checkouts.append(num)

        data = {
            'title': p.title,
            'owner': p.owner,
            'users': p.users.all(),
            'created': True if p.created >= start_date and p.created <= end_date else False,
            'expected_completion': True if p.expected_completion_date >= start_date and p.expected_completion_date <= end_date else False,
            'equipment_checkouts': checkouts
        }

        project_data['projects'].append(data)


    return project_data

def get_userprofile_data(start_date, end_date):
    profiles = UserProfile.objects.order_by('user__last_name', 'user__first_name')
    badges = Badge.objects.order_by('title')
    classes = Class.objects.order_by('class_title')
    equipment = Equipment.objects.order_by('make', 'model')

    userprofile_data = {
        'profiles': [],
        'badges': [b.title for b in badges],
        'classes': [c.class_title for c in classes],
        'equipment': [e.name() for e in equipment]
    }

    for p in profiles:
        user_badges = p.earned_badges()
        badge_indicators = []
        for b in badges:
            if b in user_badges:
                badge_indicators.append(True)
            else:
                badge_indicators.append(False)


        user_registrations = p.user.classregistration_set.all()
        class_completions = []
        for c in classes:
            ex = False
            for r in user_registrations:
                if r.class_section.class_key == c:
                    class_completions.append({
                        'completed': r.completed,
                        'score': r.score_percentage
                    })
                    ex = True
            if not ex:
                class_completions.append({
                    'completed': False,
                    'score': None
                })


        checkouts = []
        for e in equipment:
            num = p.user.equipmentcheckout_set.all().filter(
                Q(equipment=e)
                & Q(checkout_date__gte=start_date)
                & Q(checkout_date__lte=end_date)
            ).count()
            checkouts.append(num)


        data = {
            'user': p.user,
            'badges': badge_indicators,
            'classes': class_completions,
            'checkouts': checkouts,
        }

        userprofile_data['profiles'].append(data)

    return userprofile_data

@staff_member_required
def reporting(request):

    now = arrow.utcnow()
    start_date = arrow.get(datetime.datetime(now.year, 1, 1)).date()
    end_date = now.date()
    form = ReportDateRangeForm(request.POST or None, initial={
        'report_start_date': start_date,
        'report_end_date': end_date,
    })

    if form.is_valid():
        start_date = form.cleaned_data['report_start_date']
        end_date = form.cleaned_data['report_end_date']

    

    return render(
        request,
        'report.html',
        context={
            'form': form,
            'start_date': start_date,
            'end_date': end_date,

            'classes_data': get_classes_data(start_date, end_date),
            'inventory_data': get_inventory_data(start_date, end_date),
            'project_data': get_project_data(start_date, end_date),
            'userprofile_data': get_userprofile_data(start_date, end_date),
        }
    )   