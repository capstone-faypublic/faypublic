from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from userprofile.models import Badge, User


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

    prereq_badges = models.ManyToManyField(Badge,
        related_name="prerequisites",
        blank=True
    )

    awarded_badges = models.ManyToManyField(Badge, related_name="awarded")

    def __str__(self):
        return self.course_title

    def __unicode__(self):
        return self.course_title


class CourseSection(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    start_date = models.DateTimeField

    end_date = models.DateTimeField

    seat_avaliable = models.IntegerField(
        null=True,
        blank=True,
        default=6
    )

    def __str__(self):
        return self.course.course_title

    def __unicode__(self):
        return self.course.course_title


class CourseRegisteration(models.Model):
    course_section = models.ForeignKey(CourseSection, on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    completed = models.BooleanField(
        default=False
    )

    score = models.TextField(
        default="0"
    )


    def __str__(self):
        return self.course_section.course.course_title

    def __unicode__(self):
        return self.course_section.course.course_title


