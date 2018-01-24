from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ProducerUserProfile(models.Model):
    """ Compositition of Django's default User model to assign more information to users """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email_address = models.EmailField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    # class Meta:
        ## add special user permissions/groups here
        # permissions = (
        #     ('permission_or_group', 'Description')
        # )