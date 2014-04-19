import datetime

from django.conf import settings
from django.utils.timezone import now

from celery.task import task
from celery.utils.log import get_task_logger

from core.tasks import send_email, send_sms
from .models import Research, FEEDBACK_STATUS_PUNISHMENT, FEEDBACK_STATUS_PENDING, FEEDBACK_STATUS_SEND_REMIND


logger = get_task_logger(__name__)


@task
def check_feedback_promise():
    for research in Research.objects.filter(is_publish=True, is_feedback_promise=True, feedback_status__lt=FEEDBACK_STATUS_PUNISHMENT):
        if now() >= research.feedback_promise_time:
            if not research.is_feedback:
                research.feedback_status = FEEDBACK_STATUS_PUNISHMENT
                research.save()
                #TODO:Over time there is no feedback
        elif now() + datetime.timedelta(seconds=86400) >= research.feedback_promise_time:
            if research.feedback_status == FEEDBACK_STATUS_PENDING and not research.is_feedback:
                notification = {
                    'subject': 'Study of feedback reminder',
                    'recipient_list': [sr.scientist.email for sr in list(research.scientistresearch_set.all())],
                    'html_content': 'You have a study[%s] about to reach the promised time feedback, please timely feedback' % research.name
                }
                send_email.delay(notification)
                research.feedback_status = FEEDBACK_STATUS_SEND_REMIND
                research.save()


@task
def send_notifications_for_scientists():
    for research in Research.objects.filter(is_publish=True, is_on_web=False, remind_research=True):
        event = research.get_nearest_event()
        if event and not event.is_scientist_sent:
            for remind_scientist in research.remindscientistinfo_set.all():
                seconds = remind_scientist.get_remind_scientist_time()
                if now() + datetime.timedelta(seconds=seconds) >= event.start:
                    logger.info('Generate a notification for %s' % research.name)
                    event.is_scientist_sent = True
                    if remind_scientist.type == 'email':
                        _send_email(research, remind_scientist)
                    elif remind_scientist.type == 'sms':
                        _send_sms(research, remind_scientist)
                    else:
                        logger.info('Notification type is incorrect')
            event.save()
    return True


def _send_email(research, remind_scientist):
    notification = {
        'subject': remind_scientist.message,
        'recipient_list': [sr.scientist.email for sr in list(research.scientistresearch_set.all())],
        'html_content': remind_scientist.message
    }

    send_email.delay(notification)


def _send_sms(research, remind_scientist):
    recipient_list = []
    for sr in list(research.scientistresearch_set.all()):
        basic_info = sr.scientist.userprofile.basic_info
        scientist_info = basic_info.get('scientist', {}) if basic_info else {}
        mobile = scientist_info.get('mobile', None)
        if mobile:
            recipient_list.append(filter(lambda x: x.strip() != "", mobile))

    notification = {
        'subject': remind_scientist.message,
        'recipient_list': recipient_list,
        'html_content': remind_scientist.message,
        'account_sid': settings.TWILIO_ACCOUNT_SID,
        'auth_token': settings.TWILIO_AUTH_TOKEN,
        'from_number': settings.TWILIO_FROM_NUMBER,
    }

    send_sms.delay(notification)