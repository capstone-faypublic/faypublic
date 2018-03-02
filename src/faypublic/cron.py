from django.core.mail import send_mail
from django_cron import CronJobBase, Schedule

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'faypublic.my_cron_job'    # a unique code

    def do(self):
        pass    # do your thing here
        send_mail(
            'Subject here',
            'Here is the message.',
            'miamigarrett@yahoo.com',
            ['gwadegraham@gmail.com'],
            fail_silently=False,
        )