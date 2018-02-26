from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Course(models.Model):
    course_title = models.CharField(
        max_length=255,
        null=True,
        blank=False,
    )

    course_description = models.TextField(
        null=True,
        blank=False
    )

    course_duration = models.CharField(
        max_length=255,
        null=True,
        blank=False
    )

    course_capacity = models.IntegerField(
        null=True,
        blank=False
    )




class PrerequisiteCourses(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_prerequisites = models.ManyToManyField(Course)
    # needed_course = models.ForeignKey(Course.course_title, on_delete=models.CASCADE)
    # course_id = models.ForeignKey(Course)
    # needed_course = models.ForeignKey(Course)
