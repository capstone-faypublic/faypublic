# Generated by Django 2.0.1 on 2018-02-24 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('equipmentcheckout', '0010_remove_equipment_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='equipmentcheckout.EquipmentCategory'),
        ),
    ]