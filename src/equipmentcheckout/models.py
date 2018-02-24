from django.db import models
from django.contrib.auth.models import User
from project.models import Project
from django.template.defaultfilters import slugify

# AUDIO = 'AUDIO'
# VIDEO = 'VIDEO'
# LIGHTING = 'LIGHTING'
# EQUIPMENT_CATEGORIES = [
#     (AUDIO, 'Audio'),
#     (VIDEO, 'Video'),
#     (LIGHTING, 'Lighting')
# ]


CHECKOUT_24HR = 'CHECKOUT_24HR'
CHECKOUT_WEEK = 'CHECKOUT_WEEK'
CHECKOUT_TIMEFRAMES = [
    (CHECKOUT_24HR, '24hr checkout'),
    (CHECKOUT_WEEK, 'Thurs-Tues checkout')
]



class EquipmentCategory(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(EquipmentCategory, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return '/equipment/category/' + self.slug

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title



def handle_file_upload(instance, filename):
    return 'uploads/equip_{0}/{1}'.format(instance.id, filename)

class Equipment(models.Model):
    make = models.CharField(max_length=255, null=True, blank=False)
    model = models.CharField(max_length=255, null=True, blank=False)
    slug = models.SlugField(blank=True)
    quantity = models.IntegerField()
    description = models.TextField(null=True, blank=True)

    category = models.ForeignKey(EquipmentCategory, on_delete=models.CASCADE)

    checkout_timeframe = models.CharField(max_length=15, choices=CHECKOUT_TIMEFRAMES, default=CHECKOUT_WEEK)
    image = models.FileField(upload_to=handle_file_upload, null=True)
    manual_url = models.URLField(null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.make + " " + self.model)
        super(Equipment, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return '/equipment/' + self.slug

    def __unicode__(self):
        return self.make + " " + self.model

    def __str__(self):
        return self.make + " " + self.model


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
