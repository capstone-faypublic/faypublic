from django.forms import Form, ModelForm
from .models import UserProfile

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']