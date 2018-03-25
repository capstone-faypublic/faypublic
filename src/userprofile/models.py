from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def get_user_display_name(self):
    return self.first_name + ' ' + self.last_name + ' [' + self.username + ']'
User.add_to_class('__str__', get_user_display_name)
User.add_to_class('__unicode__', get_user_display_name)

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
        registrations = self.user.classregistration_set.filter(completed=True)
        badges = []

        for reg in registrations:
            sect = reg.class_section
            course = sect.class_key
            for badge in course.awarded_badges.all():
                if not badge in badges:
                    badges.append(badge)

        return badges



class Badge(models.Model):
    title = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title