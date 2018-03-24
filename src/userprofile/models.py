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


    def earned_badges(self):
        # classes = self.user.classregistration_set.filter(completed=True)
        registrations = self.user.classregistration_set.all()
        # return registrations
        badges = []

        for reg in registrations:
            sect = reg.class_section
            course = sect.class_key
            for badge in course.awarded_badges.all():
                if not badge in badges:
                    badges.append(badge)

        return badges



class Badge(models.Model):
    badge = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )