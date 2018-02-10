from django.db import models
from userprofile.models import UserProfile

# Create your models here.
class Project(models.Model):
    users = models.ManyToManyField(UserProfile)

    title = models.CharField(
        max_length=255, 
        null=True,
        blank=False
    )

    created_on = models.DateField(auto_now_add=True)

    def get_absolute_url(self):
        return "/projects/%i/" % self.id

    def recent_submissions(self):
        return self.projectsubmission_set.all()[:3]


    # many to many field with equipment checkout model
    # equipment_checkouts = models.ManyToManyField(EquipmentCheckout)
    # inside and outside projects will rely on this



def handle_file_upload(instance, filename):
    return 'uploads/project_{0}/{1}'.format(instance.project.id, filename)


class ProjectSubmission(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    title = models.CharField(
        max_length=255, 
        null=True,
        blank=False
    )

    uploaded_file = models.FileField(upload_to=handle_file_upload)