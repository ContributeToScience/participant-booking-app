from department.models import ParticipantCreditScheme
from django import template
from scientist.models import ParticipantResearch

register = template.Library()


@register.simple_tag
def show_participant_name(research, participant_research):
    username = participant_research.participant.userprofile.get_full_name()
    if research.is_anonymous:
        username = '%s**%s' % (username[0], username[-1])
    return username


@register.simple_tag
def get_take_part_research_count(participant):
    return ParticipantResearch.objects.filter(participant=participant, confirmed=True).count()


@register.simple_tag
def get_take_part_department_count(participant):
    return ParticipantCreditScheme.objects.filter(participant=participant).count()


@register.simple_tag
def get_payment_message_count(participant):
    return ParticipantResearch.objects.filter(participant=participant, confirmed=True,
                                              award_credit__gt=0, scientist_award_dt__isnull=False,
                                              participant_resp__isnull=True,
                                              participant_resp_dt__isnull=True).count()