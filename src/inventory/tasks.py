import arrow
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import EquipmentCheckout
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name='task_send_equipment_checkout_reminder_email',
    ignore_result=True
)
def send_equipment_checkout_reminder_email():
    today = arrow.utcnow().date()
    due_today = EquipmentCheckout.objects.filter(due_date=today)

    logger.info('attempting to send emails...')
    print('attempting to send emails...')
    
    for reg in due_today:
        user = reg.user
        send_mail(
            'Reminder: Your equipment is due today!',
            '''
                Greetings''' + user.first_name + ''',\n
                Quick reminder that your equipment checkout of ''' + reg.equipment.make + ' ' + reg.equipment.model + ''' is due today!\n
                Please return your checked out item by 5 p.m. today.\n
                Thank you!\n\n
                Fayetteville Public Television\n\n
                You're receiving this email because you've asked to be notified when your equipment is due. You can change this setting in <a href="https://domain.com/profile/">Your profile</a>
            ''',
            'timpe31@gmail.com',
            [user.email],
            fail_silently=False
        )