from django.db import models
from userprofile.models import UserProfile
from django.contrib.auth.models import User

SUBMITTED = 'SUBMITTED'
SCHEDULED = 'SCHEDULED'
REJECTED = 'REJECTED'

PROGRAM_REQUEST_STATUS = (
    (SUBMITTED, 'Submitted'),
    (SCHEDULED, 'Approved'),
    (REJECTED, 'Rejected')
)


def handle_file_upload(instance, filename):
    return 'uploads/project_{0}/{1}'.format(instance.project.id, filename)


class Project(models.Model):
    class Meta:
        verbose_name = "project"
        verbose_name_plural = "projects"

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_projects')
    users = models.ManyToManyField(User)
    title = models.CharField(max_length=255, null=True, blank=False)
    created = models.DateField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    expected_completion_date = models.DateField(null=True, blank=False)
    uploaded_file = models.FileField(upload_to=handle_file_upload, null=True, blank=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/profile/projects/%i/" % self.id



class ProgramRequest(models.Model):
    class Meta:
        verbose_name = "program request"
        verbose_name_plural = "program requests"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=False)
    description = models.TextField(null=True, blank=True)
    requested_on = models.DateField(auto_now_add=True)
    requested_play_date = models.DateTimeField(null=True, blank=False)
    media_link = models.URLField(null=True, blank=False)
    status = models.CharField(
        max_length = 20,
        choices = PROGRAM_REQUEST_STATUS,
        default = SUBMITTED
    )


    def __str__(self):
        return self.title
    
    def __unicode__(self):
        return self.title