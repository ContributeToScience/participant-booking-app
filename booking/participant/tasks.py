import datetime

from django.conf import settings
from django.utils.timezone import now

from celery.task import task
from celery.utils.log import get_task_logger

from core.tasks import send_email, send_sms
from scientist.models import Research, ParticipantResearchEvent

logger = get_task_logger(__name__)


@task
def send_notifications_for_participants():
    for research in Research.objects.filter(is_publish=True, is_on_web=False, remind_participant=True):
        event = research.get_nearest_event()
        if event and not event.is_participant_sent:
            for remind_participant in research.remindparticipantinfo_set.all():
                seconds = remind_participant.get_remind_participant_time()
                if now() + datetime.timedelta(seconds=seconds) >= event.start:
                    logger.info('Generate a notification for %s' % research.name)
                    event.is_participant_sent = True
                    if remind_participant.type == 'email':
                        _send_email(research, remind_participant, event)
                    elif remind_participant.type == 'sms':
                        _send_sms(research, remind_participant, event)
                    else:
                        logger.info('Notification type is incorrect')
            event.save()
    return True


def _send_email(research, remind_participant, event):
    recipient_list = []
    for pr in list(research.participantresearch_set.filter(confirmed=True)):
        participant_event = ParticipantResearchEvent.objects.filter(research_event=event,
                                                                    participant=pr.participant)
        if participant_event:
            recipient_list.append(participant_event[0].participant.email)

    notification = {
        'subject': remind_participant.message,
        'recipient_list': recipient_list,
        'html_content': remind_participant.message
    }

    send_email.delay(notification)


def _send_sms(research, remind_participant, event):
    recipient_list = []

    for pr in list(research.participantresearch_set.filter(confirmed=True)):
        participant_event = ParticipantResearchEvent.objects.filter(research_event=event,
                                                                    participant=pr.participant)
        if participant_event:
            basic_info = participant_event[0].participant.userprofile.basic_info
            participant_info = basic_info.get('participant', {}) if basic_info else {}
            mobile = participant_info.get('mobile', None)
            if mobile:
                recipient_list.append(filter(lambda x: x.strip() != "", mobile))

    notification = {
        'subject': remind_participant.message,
        'recipient_list': recipient_list,
        'html_content': remind_participant.message,
        'account_sid': settings.TWILIO_ACCOUNT_SID,
        'auth_token': settings.TWILIO_AUTH_TOKEN,
        'from_number': settings.TWILIO_FROM_NUMBER,
    }

    send_sms.delay(notification)