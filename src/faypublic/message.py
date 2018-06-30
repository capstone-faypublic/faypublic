import arrow


def datetime_format(dt):
    return arrow.get(dt).format('dddd MMM D, YYYY h:mm a')


# Equipment pickup reminders

def equipment_pickup_reminder_email(userprofile, checkout):
    subject = 'Reminder: check out your equipment today! ~ FPTV'
    message_body = '''Greetings, ''' + userprofile.user.first_name + ''',\n
This is a reminder that the ''' + checkout.equipment_name() + ''' you have reserved for checkout can be picked up today.\n
The Fayetteville Public Television office is open from 10am-7pm on Monday, Tuesday, Thursday, Friday, and Saturday.\n\n
Checkout details:
Item: ''' + checkout.equipment.make + ' ' + checkout.equipment.model + '''
Checkout Date: ''' + datetime_format(checkout.checkout_date) + '''
Return Date: ''' + datetime_format(checkout.due_date) + ''' (''' + checkout.due_date_humanized() + ''')
Project: ''' + checkout.project_title() + '''
Checkout to: ''' + checkout.user_name() + '''\n\n
Please remember to return your equipment by the due date listed above. Thank you!\n
Fayetteville Public Television
(479) 444-3433
101 West Rock Street, Fayetteville, AR 72701\n\n
You are receiving this email because you have subscribed to email notifications via https://login.faypublic.tv
'''
    return subject, message_body


def equipment_pickup_reminder_sms(userprofile, checkout):
    return '''Hello, ''' + userprofile.user.first_name + '''
This is a reminder that the ''' + checkout.equipment_name() + ''' you have reserved for checkout can be picked up today!\n
~ FPTV | (479) 444-3433
'''

##

# Equipment due reminders

def equipment_due_reminder_email(userprofile, checkout):
    subject = 'Reminder: your equipment is due today! ~ FPTV'
    message_body = '''Greetings, ''' + userprofile.user.first_name + ''',\n
This is a reminder that the ''' + checkout.equipment_name() + ''' you have checked out needs to be returned today.\n
The Fayetteville Public Television office is open from 10am-7pm on Monday, Tuesday, Thursday, Friday, and Saturday.\n\n
Checkout details:
Item: ''' + checkout.equipment.make + ' ' + checkout.equipment.model + '''
Checkout Date: ''' + datetime_format(checkout.checkout_date) + '''
Return Date: ''' + datetime_format(checkout.due_date) + ''' (''' + checkout.due_date_humanized() + ''')
Project: ''' + checkout.project_title() + '''
Checked out to: ''' + checkout.user_name() + '''\n\n
You have until the office closes today to return this item. Thank you!\n
Fayetteville Public Television
(479) 444-3433
101 West Rock Street, Fayetteville, AR 72701\n\n
You are receiving this email because you have subscribed to email notifications via https://login.faypublic.tv
'''
    return subject, message_body


def equipment_due_reminder_sms(userprofile, checkout):
    return '''Hello, ''' + userprofile.user.first_name + '''
This is a reminder that the ''' + checkout.equipment_name() + ''' you have checked out is due back today!\n
~ FPTV | (479) 444-3433
'''

##

# Equipment overdue notifications

def equipment_overdue_notification_email(userprofile, checkout):
    subject = 'Equipment OVERDUE ~ FPTV'
    message_body = '''Hey, ''' + userprofile.user.first_name + ''',\n
Our records are indicating that you have an item checked out past its due date. Please return it as soon as possible, or call us at (479) 444-3433 and request an extension.\n
The Fayetteville Public Television office is open from 10am-7pm on Monday, Tuesday, Thursday, Friday, and Saturday.\n\n
Checkout details:
Item: ''' + checkout.equipment.make + ' ' + checkout.equipment.model + '''
Checkout Date: ''' + datetime_format(checkout.checkout_date) + '''
Return Date: ''' + datetime_format(checkout.due_date) + ''' (''' + checkout.due_date_humanized() + ''')
Project: ''' + checkout.project_title() + '''
Checked out to: ''' + checkout.user_name() + '''\n\n
Fayetteville Public Television
(479) 444-3433
101 West Rock Street, Fayetteville, AR 72701\n\n
You are receiving this email because you have subscribed to email notifications via https://login.faypublic.tv
'''
    return subject, message_body


def equipment_overdue_notification_sms(userprofile, checkout):
    return userprofile.user.first_name + ''', you have an item checked out past its due date. ''' + checkout.equipment_name() + ''' must be returned as soon as possible.\n
~ FPTV | (479) 444-3433
'''

## 

## Class registration reminder

def class_registration_reminder_email(userprofile, registration):
    subject = 'Reminder: you have class today! ~ FPTV'
    message_body = '''Greetings, ''' + userprofile.user.first_name + ''',\n
This is a reminder that the class you're registered for, ''' + registration.class_title() + ''', is today!\n
Registration details:
Class: ''' + registration.class_title() + '''
Class Date: ''' + datetime_format(registration.section()) + '''\n\n
We're excited to see you there!\n
Fayetteville Public Television
(479) 444-3433
101 West Rock Street, Fayetteville, AR 72701\n\n
You are receiving this email because you have subscribed to email notifications via https://login.faypublic.tv
'''
    return subject, message_body

def class_registration_reminder_sms(userprofile, registration):
    return ''' Hello, ''' + userprofile.user.first_name + '''
This is a reminder that the class you're registered for, ''' + registration.class_title() + ''', is today! Can't wait to see you there!
Class date: ''' + datetime_format(registration.section()) + '''\n
~ FPTV | (479) 444-3433
'''