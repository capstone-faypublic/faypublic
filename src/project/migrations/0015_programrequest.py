# Generated by Django 2.0.1 on 2018-04-18 16:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0014_auto_20180418_1008'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgramRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('requested_on', models.DateField(auto_now_add=True)),
                ('requested_play_date', models.DateTimeField(null=True)),
                ('media_link', models.URLField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_program_requests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'program request',
                'verbose_name_plural': 'program requests',
            },
        ),
    ]
