# Generated by Django 2.0.1 on 2018-07-22 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0011_auto_20180429_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='is_by_appointment',
            field=models.BooleanField(default=False),
        ),
    ]
