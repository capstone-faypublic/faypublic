# Generated by Django 2.0.1 on 2018-03-25 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_badge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='badge',
            old_name='badge',
            new_name='title',
        ),
    ]
