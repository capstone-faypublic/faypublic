# Generated by Django 2.0.1 on 2018-03-10 19:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import inventory.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0010_project_expected_completion_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=255, null=True)),
                ('model', models.CharField(max_length=255, null=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('quantity', models.IntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('checkout_timeframe', models.CharField(choices=[('CHECKOUT_24HR', '24hr checkout'), ('CHECKOUT_WEEK', 'Thurs-Tues checkout')], default='CHECKOUT_WEEK', max_length=15)),
                ('image', models.FileField(null=True, upload_to=inventory.models.handle_file_upload)),
                ('manual_url', models.URLField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'equipment',
                'verbose_name_plural': 'inventory',
            },
        ),
        migrations.CreateModel(
            name='EquipmentCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='EquipmentCheckout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkout_date', models.DateField(null=True)),
                ('due_date', models.DateField(null=True)),
                ('checkout_status', models.CharField(choices=[('RESERVED', 'Reserved'), ('CHECKED_OUT', 'Checked Out'), ('RETURNED', 'Returned')], default='RESERVED', max_length=15)),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Equipment')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'checkout',
                'verbose_name_plural': 'checkouts',
            },
        ),
        migrations.AddField(
            model_name='equipment',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.EquipmentCategory'),
        ),
    ]
