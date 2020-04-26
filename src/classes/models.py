from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models import Q
import arrow

# Create your models here.
from userprofile.models import Badge, UserProfile


class Class(models.Model):
    class Meta:
        verbose_name = "class"
        verbose_name_plural = "classes"

    class_title = models.CharField(max_length=255, null=True, blank=False)
    class_description = models.TextField(null=True, blank=False)
    prerequisite_badges = models.ManyToManyField(Badge, related_name="courses_with_badge_prerequisite", blank=True)
    awarded_badges = models.ManyToManyField(Badge, related_name="courses_with_badge_awarded", blank=True)
    slug = models.SlugField(blank=True, unique=True)
    is_by_appointment = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.class_title)
        super(Class, self).save(*args, **kwargs)

    def __str__(self):
        return self.class_title

    def __unicode__(self):
        return self.class_title

    def get_register_url(self):
        return '/classes/' + self.slug

    def get_open_sections(self):
        return self.classsection_set.filter(
            Q(date__gte=arrow.utcnow().datetime)
        ).order_by('date')

    def number_of_open_sections(self):
        return len(self.get_open_sections())


class ClassSection(models.Model):
    class Meta:
        verbose_name = "section"
        verbose_name_plural = "sections"

    class_key = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateTimeField()
    seats_available = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.class_key.class_title + ' - ' + arrow.get(self.date).format('MM/DD/YYYY HH:mm')

    def __unicode__(self):
        return self.class_key.class_title + ' - ' + arrow.get(self.date).format('MM/DD/YYYY HH:mm')

    def number_open_seats(self):
        return self.seats_available - len(self.classregistration_set.all())

    def number_registered(self):
        return len(self.classregistration_set.all())
 
    def date_humanized(self):
        return arrow.get(self.date).humanize(arrow.utcnow())


class ClassRegistration(models.Model):
    class Meta:
        verbose_name = "registration"
        verbose_name_plural = "registrations"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class_section = models.ForeignKey(ClassSection, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    score_percentage = models.DecimalField(null=True, blank=True, max_digits=4, decimal_places=1)

    def class_title(self):
        return self.class_section.class_key.class_title
    
    def section(self):
        return self.class_section.date

    def __str__(self):
        return self.class_section.class_key.class_title

    def __unicode__(self):
        return self.class_section.class_key.class_title


