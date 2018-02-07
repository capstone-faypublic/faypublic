from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # additional user information we want to collect
    street_address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    zipcode = models.IntegerField(null=True)

    phone_number = models.CharField(max_length=15, null=True)
    birthdate = models.DateField(null=True)