from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class EquipmentCheckout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # equipmentID = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    # projectID = models.ForeignKey(Project, on_delete=models.CASCADE)

    # additional equipment checkout information we want to collect
    checkout_date = models.DateField(null=True)
    due_date = models.DateField(null=True)
    RESERVED = 'RE'
    CHECKED_OUT = 'CO'
    RETURNED = 'RT'
    CHECKOUT_STATUS_CHOICES = (
        (RESERVED, 'Reserved'),
        (CHECKED_OUT, 'Checked Out'),
        (RETURNED, 'Returned'),
    )
    checkout_status = models.CharField(
        max_length=2,
        choices = CHECKOUT_STATUS_CHOICES,
        default = RESERVED,
    )
