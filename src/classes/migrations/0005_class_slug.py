# Generated by Django 2.0.1 on 2018-03-12 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0004_auto_20180312_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='slug',
            field=models.SlugField(default='fff'),
            preserve_default=False,
        ),
    ]
