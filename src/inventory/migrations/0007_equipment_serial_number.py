# Generated by Django 2.0.1 on 2018-04-21 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20180418_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='serial_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
