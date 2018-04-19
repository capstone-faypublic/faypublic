import arrow
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from django.core.mail import send_mail
from django.contrib.auth.models import User
from inventory.models import EquipmentCheckout
from classes.models import ClassRegistration
from userprofile.models import UserProfile
from celery.utils.log import get_task_logger
from twilio.rest import Client
from .settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from .message import equipment_pickup_reminder_email, equipment_pickup_reminder_sms, equipment_due_reminder_email, equipment_due_reminder_sms, equipment_overdue_notification_email, equipment_overdue_notification_sms, class_registration_reminder_email, class_registration_reminder_sms
from django.db.models import Q

logger = get_task_logger(__name__)

# to run celery in development mode, open two terminal windows and execute the following (one command per window)
# docker-compose exec django celery -A faypublic worker -l info
# docker-compose exec django celery -A faypublic beat -l info



# Equipment checkout reminder

@periodic_task(
    # run_every=(crontab(minute=0, hour=19)), # run every day at 9am
    run_every=(crontab(minute='*/1')), # run every minute
    name='task_send_equipment_pickup_reminder',
    ignore_result=True
)
def send_equipment_pickup_reminder():
    today = arrow.utcnow().datetime
    check_out_today = EquipmentCheckout.objects.filter(
        Q(checkout_date__gte=arrow.utcnow().replace(hour=0, minute=0, second=0).datetime)
        & Q(checkout_date__lte=arrow.utcnow().replace(hour=23, minute=59, second=59).datetime)
        & Q(checkout_status='RESERVED')
    )

    logger.info('Run task: task_send_equipment_pickup_reminder')
    print('Run task: task_send_equipment_pickup_reminder')

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    for checkout in check_out_today:
        user = checkout.user
        profile = UserProfile.objects.get(user=user)

        if profile.get_email_reminders:
            subj, msg = equipment_pickup_reminder_email(profile, checkout)
            send_mail(
                subject=subj,
                message=msg,
                from_email='timpe31@gmail.com',
                recipient_list=[user.email],
                fail_silently=True,
            )
        
        if profile.get_sms_reminders:
            msg = equipment_pickup_reminder_sms(profile, checkout)
            try:
                message = client.messages.create(
                    to=profile.phone_number,
                    from_='+19728107378',
                    body=msg
                )
            except:
                logger.info('Failed to send to ' + profile.phone_number + ' - invalid number')
                print('Failed to send to ' + profile.phone_number + ' - invalid number')

##

## Equipment due reminder

@periodic_task(
    # run_every=(crontab(minute=0, hour=19)), # run every day at 9am
    run_every=(crontab(minute='*/1')), # run every minute
    name='task_send_equipment_due_reminder',
    ignore_result=True
)
def send_equipment_due_reminder():
    today = arrow.utcnow().datetime
    check_out_today = EquipmentCheckout.objects.filter(
        Q(due_date__gte=arrow.utcnow().replace(hour=0, minute=0, second=0).datetime)
        & Q(due_date__lte=arrow.utcnow().replace(hour=23, minute=59, second=59).datetime)
        & Q(checkout_status='CHECKED_OUT')
    )

    logger.info('Run task: task_send_equipment_due_reminder')
    print('Run task: task_send_equipment_due_reminder')

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    for checkout in check_out_today:
        user = checkout.user
        profile = UserProfile.objects.get(user=user)

        if profile.get_email_reminders:
            subj, msg = equipment_due_reminder_email(profile, checkout)
            send_mail(
                subject=subj,
                message=msg,
                from_email='timpe31@gmail.com',
                recipient_list=[user.email],
                fail_silently=True,
            )
        
        if profile.get_sms_reminders:
            msg = equipment_due_reminder_sms(profile, checkout)
            try:
                message = client.messages.create(
                    to=profile.phone_number,
                    from_='+19728107378',
                    body=msg
                )
            except:
                logger.info('Failed to send to ' + profile.phone_number + ' - invalid number')
                print('Failed to send to ' + profile.phone_number + ' - invalid number')

##

## Equipment overdue notification

@periodic_task(
    # run_every=(crontab(minute=0, hour=19)), # run every day at 9am
    run_every=(crontab(minute='*/1')), # run every minute
    name='task_send_equipment_overdue_notification',
    ignore_result=True
)
def send_equipment_overdue_notification():
    today = arrow.utcnow().datetime
    check_out_today = EquipmentCheckout.objects.filter(
        Q(due_date__lte=arrow.utcnow().replace(hour=0, minute=0, second=0).datetime)
        & Q(checkout_status='CHECKED_OUT')
    )

    logger.info('Run task: task_send_equipment_overdue_notification')
    print('Run task: task_send_equipment_overdue_notification')

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    for checkout in check_out_today:
        user = checkout.user
        profile = UserProfile.objects.get(user=user)

        if profile.get_email_reminders:
            subj, msg = equipment_overdue_notification_email(profile, checkout)
            send_mail(
                subject=subj,
                message=msg,
                from_email='timpe31@gmail.com',
                recipient_list=[user.email],
                fail_silently=True,
            )
        
        if profile.get_sms_reminders:
            msg = equipment_overdue_notification_sms(profile, checkout)
            try:
                message = client.messages.create(
                    to=profile.phone_number,
                    from_='+19728107378',
                    body=msg
                )
            except:
                logger.info('Failed to send to ' + profile.phone_number + ' - invalid number')
                print('Failed to send to ' + profile.phone_number + ' - invalid number')

##

@periodic_task(
    # run_every=(crontab(minute=0, hour=19)), # run every day at 9am
    run_every=(crontab(minute='*/1')), # run every minute
    name='task_send_class_registration_reminder',
    ignore_result=True
)
def send_class_registration_reminder():
    today = arrow.utcnow().date()
    check_out_today = ClassRegistration.objects.filter(
        Q(class_section__date__gte=arrow.utcnow().replace(hour=0, minute=0, second=0).datetime)
        & Q(class_section__date__lte=arrow.utcnow().replace(hour=23, minute=59, second=59).datetime)
    )

    logger.info('Run task: task_send_class_registration_reminder')
    print('Run task: task_send_class_registration_reminder')

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    for checkout in check_out_today:
        user = checkout.user
        profile = UserProfile.objects.get(user=user)

        if profile.get_email_reminders:
            subj, msg = class_registration_reminder_email(profile, checkout)
            send_mail(
                subject=subj,
                message=msg,
                from_email='timpe31@gmail.com',
                recipient_list=[user.email],
                fail_silently=True,
            )
        
        if profile.get_sms_reminders:
            msg = class_registration_reminder_sms(profile, checkout)
            # try:
            message = client.messages.create(
                to=profile.phone_number,
                from_='+19728107378',
                body=msg
            )
            except:
                # logger.info('Failed to send to ' + profile.phone_number + ' - invalid number')
                # print('Failed to send to ' + profile.phone_number + ' - invalid number')