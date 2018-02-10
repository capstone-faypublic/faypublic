# Generated by Django 2.0.1 on 2018-02-10 21:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_auto_20180210_2032'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='created_on',
            new_name='created',
        ),
        migrations.AddField(
            model_name='projectsubmission',
            name='created',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectsubmission',
            name='status',
            field=models.CharField(choices=[('SUBMITTED', 'Submitted. Waiting for administrator review.'), ('SCHEDULED', 'Approved! Your request has been approved and scheduled.'), ('REJECTED', "Oops, we couldn't accept this request.")], default='SUBMITTED', max_length=15),
        ),
        migrations.AddField(
            model_name='projectsubmission',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]