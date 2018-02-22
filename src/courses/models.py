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

#     course_prerequisites = models.ManyToManyField(PrerequisiteCourses)
#
#
# class PrerequisiteCourses(models.Model):
#     course_id = models.ForeignKey(Course, on_delete=models.CASCADE())
#     needed_course = models.ForeignKey(Course, on_delete=models.CASCADE())
