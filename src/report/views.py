import arrow, datetime
from django.shortcuts import render
from .forms import ReportDateRangeForm
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

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
        }
    )