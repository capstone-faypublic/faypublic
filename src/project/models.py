import arrow, os
from django.db import models
from userprofile.models import UserProfile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from faypublic.settings import DEBUG

SUBMITTED = 'SUBMITTED'
SCHEDULED = 'SCHEDULED'
REJECTED = 'REJECTED'

PROGRAM_REQUEST_STATUS = (
    (SUBMITTED, 'Submitted'),
    (SCHEDULED, 'Approved'),
    (REJECTED, 'Rejected')
)


def handle_file_upload(project, filename):
    timestamp = arrow.utcnow().timestamp
    return 'uploads/{0}/project-uploads/{1}-{2}'.format(project.owner.username, timestamp, filename)


def validate_video_extension(file):
    valid_extensions = ['.mp4']
    ext = os.path.splitext(file.name)[1]
    if not ext.lower() in valid_extensions:
        raise ValidationError('Invalid file type; please use .mp4')


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
    uploaded_file = models.FileField(upload_to=handle_file_upload, null=True, blank=True, validators=[validate_video_extension])

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/profile/projects/%i/" % self.id

    def get_uploaded_file_url(self):
        if DEBUG:
            return '/static/media/' + self.uploaded_file.url
        return self.uploaded_file.url



class ProgramRequest(models.Model):
    class Meta:
        verbose_name = "program request"
        verbose_name_plural = "program requests"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=False)
    description = models.TextField(null=True, blank=True)
    requested_on = models.DateField(auto_now_add=True)
    requested_play_date = models.DateTimeField(null=True, blank=False)
    media_link = models.URLField(max_length=500, null=True, blank=False)
    status = models.CharField(
        max_length = 20,
        choices = PROGRAM_REQUEST_STATUS,
        default = SUBMITTED
    )
    contains_mature_content = models.BooleanField(default=False)


    def __str__(self):
        return self.title
    
    def __unicode__(self):
        return self.title