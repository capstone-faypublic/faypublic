from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import Form, ModelForm

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

        # Adding placeholder text
        self.fields['username'].widget.attrs['placeholder'] = ('Username')
        self.fields['first_name'].widget.attrs['placeholder'] = ('First Name')
        self.fields['last_name'].widget.attrs['placeholder'] = ('Last Name')
        self.fields['email'].widget.attrs['placeholder'] = ('Email')
        self.fields['password1'].widget.attrs['placeholder'] = ('Password')
        self.fields['password2'].widget.attrs['placeholder'] = ('Confirm Password')

        # Removing help text
        for fieldname in ['username', 'password2']:
        	self.fields[fieldname].help_text = None
        for fieldname in ['password1']:
        	self.fields[fieldname].help_text = "Must contain 8 characters, with at least 1 letter"

       	# Removing labels 
        for fieldname in ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']:
        	self.fields[fieldname].label = ""