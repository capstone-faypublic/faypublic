# Generated by Django 2.0.1 on 2018-02-25 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipmentcheckout', '0024_auto_20180225_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipmentcheckout',
            name='checkout_status',
            field=models.CharField(choices=[('RESERVED', 'Reserved'), ('CHECKED_OUT', 'Checked Out'), ('RETURNED', 'Returned')], default='RESERVED', max_length=15),
        ),
    ]
