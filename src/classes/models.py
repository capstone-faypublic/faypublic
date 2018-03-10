from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from userprofile.models import Badge, User


class Class(models.Model):
    class Meta:
        verbose_name = "class"
        verbose_name_plural = "classes"

    class_title = models.CharField(max_length=255, null=True, blank=False)
    class_description = models.TextField(null=True, blank=False)
    prerequisite_badges = models.ManyToManyField(Badge, related_name="prerequisites", null=True, blank=True)
    awarded_badges = models.ManyToManyField(Badge, related_name="awarded")

    def __str__(self):
        return self.class_title

    def __unicode__(self):
        return self.class_title


class ClassSection(models.Model):
    class Meta:
        verbose_name = "section"
        verbose_name_plural = "sections"

    class_key = models.ForeignKey(Class, on_delete=models.CASCADE)
    start_date = models.DateTimeField
    end_date = models.DateTimeField
    seat_avaliable = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.class_key.class_title

    def __unicode__(self):
        return self.class_key.class_title


class ClassRegistration(models.Model):
    class Meta:
        verbose_name = "registration"
        verbose_name_plural = "registrations"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class_section = models.ForeignKey(ClassSection, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    score_percentage = models.DecimalField(null=True, blank=True, max_digits=4, decimal_places=1)

    def __str__(self):
        return self.class_section.class_key.class_title

    def __unicode__(self):
        return self.class_section.class_key.class_title


