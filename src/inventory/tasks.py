import arrow
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import EquipmentCheckout
from userprofile.models import UserProfile
from celery.utils.log import get_task_logger
from twilio.rest import Client
from faypublic.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN

logger = get_task_logger(__name__)

# to run celery in development mode, open two terminal windows and execute the following (one command per window)
# docker-compose exec django celery -A faypublic worker -l info
# docker-compose exec django celery -A faypublic beat -l info

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
            subject='Reminder: Your equipment is due today!',
            message='''Greetings, ''' + user.first_name + ''',\n
This is a quick reminder that the ''' + reg.equipment.make + ' ' + reg.equipment.model + ''' you have checked out is due today! Please return your checked out item by 5 p.m.\n
Thank you!\n\n
Fayetteville Public Television\n\n
You're receiving this email because you've asked to be notified when your equipment is due. You can change this setting in your profile at https://domain.com/profile/''',
            from_email='timpe31@gmail.com',
            recipient_list=[user.email],
            fail_silently=True,
            html_message='''Greetings, ''' + user.first_name + ''',<br/>
This is a quick reminder that the ''' + reg.equipment.make + ' ' + reg.equipment.model + ''' you have checked out is due today! Please return your checked out item by 5 p.m.<br/>
Thank you!<br/><br/>
Fayetteville Public Television<br/><br/>
You're receiving this email because you've asked to be notified when your equipment is due. You can change this setting in <a href="https://domain.com/profile/">Your profile</a>'''
        )


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name='task_send_equipment_checkout_reminder_sms',
    ignore_result=True
)
def send_equipment_checkout_reminder_sms():
    today = arrow.utcnow().date()
    due_today = EquipmentCheckout.objects.filter(due_date=today)

    logger.info('attempting to send sms...')
    print('attempting to send sms...')

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    for reg in due_today:
        user = reg.user
        profile = UserProfile.objects.get(user=user)

        try:
            message = client.messages.create(
                to=profile.phone_number,
                from_='+19728107378',
                body='Hello, ' + user.first_name + ', This is a reminder that the ' + reg.equipment.make + ' ' + reg.equipment.model + ' you have checked out is due today! ~ FPTV'
            )
        except:
            print('Invalid number')