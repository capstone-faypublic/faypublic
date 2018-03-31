from django.db import models
from userprofile.models import UserProfile

SUBMITTED = 'SUBMITTED'
SCHEDULED = 'SCHEDULED'
REJECTED = 'REJECTED'

PROJECT_SUBMISSION_STATUS = (
    (SUBMITTED, 'Submitted'),
    (SCHEDULED, 'Approved'),
    (REJECTED, 'Rejected')
)


class Project(models.Model):
    class Meta:
        verbose_name = "project"
        verbose_name_plural = "projects"

    users = models.ManyToManyField(UserProfile)
    title = models.CharField(max_length=255, null=True, blank=False)
    created = models.DateField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    expected_completion_date = models.DateField(null=True, blank=False)


    def __str__(self):
        return self.title
    
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/profile/projects/%i/" % self.id

    def number_of_submissions(self):
        return len(self.projectsubmission_set.all())





def handle_file_upload(instance, filename):
    return 'uploads/project_{0}/{1}'.format(instance.project.id, filename)

class ProjectSubmission(models.Model):
    class Meta:
        verbose_name = "submission"
        verbose_name_plural = "submission"


    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=False)
    created = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    status = models.CharField(max_length=15, choices=PROJECT_SUBMISSION_STATUS, default=SUBMITTED)
    description = models.TextField(blank=True, null=True)
    admin_notes = models.TextField(blank=True, null=True)
    scheduled_time = models.DateTimeField(null=True)
    uploaded_file = models.FileField(upload_to=handle_file_upload)