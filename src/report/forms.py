from django.forms import Form
from django import forms
from functools import partial

# DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class ReportDateRangeForm(Form):
    report_start_date = forms.DateField()
    report_end_date = forms.DateField()

    def __init__(self, *args, **kwargs):
        super(ReportDateRangeForm, self).__init__(*args, **kwargs)
        self.fields['report_start_date'].widget.attrs['class'] = 'datepicker'
        self.fields['report_end_date'].widget.attrs['class'] = 'datepicker'