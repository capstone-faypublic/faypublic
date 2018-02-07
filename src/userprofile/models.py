from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # additional user information we want to collect
    street_address = models.CharField(
        max_length=255, 
        null=True,
        blank=False
    )

    city = models.CharField(
        max_length=255, 
        null=True,
        blank=False
    )

    state = models.CharField(
        max_length=255, 
        null=True,
        blank=False
    )

    zipcode = models.IntegerField(null=True, blank=False)

    phone_number = models.CharField(
        max_length=15,
        null=True,
        blank=False
    )

    birthdate = models.DateField(null=True, blank=False)