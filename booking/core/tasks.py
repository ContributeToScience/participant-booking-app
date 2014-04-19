from django.conf import settings
from django.core.mail import EmailMessage

from celery.task import task
from celery.utils.log import get_task_logger
from twilio.rest import TwilioRestClient

logger = get_task_logger(__name__)


@task
def send_email(notification):
    logger.info('Begin to send email to %s' % str(notification['recipient_list']))
    message = EmailMessage(
        subject=notification['subject'],
        body=notification['html_content'],
        #from_email=notification['from_email'],
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=notification['recipient_list']
    )

    message.content_subtype = 'html'
    message.send(fail_silently=True)

    logger.info('End to send email')

    return True


@task
def send_sms(notification):
    logger.info('Begin to send sms to %s' % str(notification['recipient_list']))
    client = TwilioRestClient(notification['account_sid'], notification['auth_token'])

    for to_number in notification['recipient_list']:
        message = client.sms.messages.create(
            body=notification['html_content'],
            to=to_number,
            from_=notification['from_number']
        )
        logger.info(message)

    logger.info('End to send sms')

    return True