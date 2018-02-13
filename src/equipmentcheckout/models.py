from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from project.models import Project

AUDIO = 'AUDIO'
VIDEO = 'VIDEO'
LIGHTING = 'LIGHTING'
EQUIPMENT_CATEGORIES = [
    (AUDIO, 'Audio'),
    (VIDEO, 'Video'),
    (LIGHTING, 'Lighting')
]

MICROPHONE = 'MICROPHONE'
WIRELESS = 'WIRELESS'
CASE = 'CASE'
STAND = 'STAND'
CABLE = 'CABLE'
HEADPHONES = 'HEADPHONES'
TELEPROMPTER = 'TELEPROMPTER'
GREEN_SCREEN = 'GREEN_SCREEN'
CAMERA = 'CAMERA'
LIGHT_KIT = 'LIGHT_KIT'
EQUIPMENT_SUBCATEGORIES = [
    (MICROPHONE, 'Microphone'),
    (WIRELESS, 'Wireless'),
    (CASE, 'Case'),
    (STAND, 'Stand'),
    (CABLE, 'Cable'),
    (HEADPHONES, 'Headphones'),
    (TELEPROMPTER, 'Teleprompter'),
    (GREEN_SCREEN, 'Green screen'),
    (CAMERA, 'Camera'),
    (LIGHT_KIT, 'Light kit')
]

CHECKOUT_24HR = 'CHECKOUT_24HR'
CHECKOUT_WEEK = 'CHECKOUT_WEEK'
CHECKOUT_TIMEFRAMES = [
    (CHECKOUT_24HR, '24hr checkout'),
    (CHECKOUT_WEEK, 'Thurs-Tues checkout')
]

class Equipment(models.Model):
    quantity = models.IntegerField()
    make = models.CharField(
        max_length=255, 
        null=True,
        blank=False
    )

    model = models.CharField(
        max_length=255, 
        null=True,
        blank=False
    )

    description = models.TextField(null=True, blank=True)

    category = models.CharField(max_length=15, choices=EQUIPMENT_CATEGORIES, default=AUDIO)

    sub_category = models.CharField(max_length=15, choices=EQUIPMENT_SUBCATEGORIES, default=MICROPHONE)

    category = models.CharField(max_length=15, choices=CHECKOUT_TIMEFRAMES, default=CHECKOUT_WEEK)

class EquipmentCheckout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    equipmentID = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    projectID = models.ForeignKey(Project, on_delete=models.CASCADE)

    # additional equipment checkout information we want to collect
    checkout_date = models.DateField(null=True)
    due_date = models.DateField(null=True)
    RESERVED = 'RE'
    CHECKED_OUT = 'CO'
    RETURNED = 'RT'
    CHECKOUT_STATUS_CHOICES = (
        (RESERVED, 'Reserved'),
        (CHECKED_OUT, 'Checked Out'),
        (RETURNED, 'Returned'),
    )
    checkout_status = models.CharField(
        max_length=2,
        choices = CHECKOUT_STATUS_CHOICES,
        default = RESERVED,
    )
