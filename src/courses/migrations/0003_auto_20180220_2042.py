# Generated by Django 2.0.1 on 2018-02-20 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20180220_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_duration',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_title',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
