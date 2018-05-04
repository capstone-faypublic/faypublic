from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'faypublic.settings')

app = Celery(
    'faypublic',
    broker="redis://redis:6379",
    backend="redis://redis:6379",
    include=['faypublic.tasks']
)
app.conf.timezone = 'America/Chicago'
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
