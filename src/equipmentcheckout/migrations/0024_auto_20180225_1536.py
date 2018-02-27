# Generated by Django 2.0.1 on 2018-02-25 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipmentcheckout', '0023_auto_20180225_1447'),
    ]

    operations = [
        migrations.RenameField(
            model_name='equipmentcheckout',
            old_name='equipmentID',
            new_name='equipment',
        ),
        migrations.RenameField(
            model_name='equipmentcheckout',
            old_name='projectID',
            new_name='project',
        ),
        migrations.AlterField(
            model_name='equipmentcheckout',
            name='checkout_status',
            field=models.CharField(choices=[('RESERVED', 'Reserved'), ('CHECKED_OUT', 'Checked Out'), ('RETURNED', 'Returned')], default='RESERVED', max_length=2),
        ),
    ]
