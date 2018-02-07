from django.db import models
from userprofile.models import UserProfile

# Create your models here.
class Project(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    title = models.CharField(
        max_length=255, 
        null=True,
        blank=False
    )


    # many to many field with equipment checkout model
    # equipment_checkouts = models.ManyToManyField(EquipmentCheckout)
    # inside and outside projects will rely on this



def handle_file_upload(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class ProjectUpload(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    title = models.CharField(
        max_length=255, 
        null=True,
        blank=False
    )

    uploaded_file = models.FileField(upload_to=handle_file_upload)