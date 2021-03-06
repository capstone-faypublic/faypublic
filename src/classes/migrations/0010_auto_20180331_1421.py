# Generated by Django 2.0.1 on 2018-03-31 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0009_auto_20180324_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='awarded_badges',
            field=models.ManyToManyField(blank=True, related_name='courses_with_badge_awarded', to='userprofile.Badge'),
        ),
        migrations.AlterField(
            model_name='class',
            name='prerequisite_badges',
            field=models.ManyToManyField(blank=True, related_name='courses_with_badge_prerequisite', to='userprofile.Badge'),
        ),
    ]
