from django import template

from scientist.models import ParticipantResearch, AnonymousDonateRecord, DonateSetting

register = template.Library()


def _get_donate_dict():
    donate_list = ParticipantResearch.objects.filter(confirmed=True,
                                                     scientist_award_dt__isnull=False, participant_resp=False,
                                                     participant_resp_dt__isnull=False)

    donate_dict = {}
    for item in donate_list:
        key = item.participant.username
        if key in donate_dict:
            donate_dict[key]['sum'] += item.donate_credit
            donate_dict[key]['count'] += 1
        else:
            donate_dict[key] = {
                'sum': item.donate_credit,
                'count': 1
            }
    return donate_dict


@register.simple_tag
def donated_total():
    total = 0
    donate_dict = _get_donate_dict()
    adr_list = [adr.donate_amount for adr in AnonymousDonateRecord.objects.all()]
    if adr_list and len(adr_list) > 0:
        total = reduce(lambda x, y: x + y, adr_list)
    for key, value in donate_dict.items():
        total += value.get('sum', 0)
    return total


@register.simple_tag
def donated_total_of_participant(participant):
    donate_dict = _get_donate_dict()
    donate = donate_dict.get(participant.username, {})
    donate_sum = donate.get('sum', 0)
    return donate_sum


@register.simple_tag
def donated_number_of_participant(participant):
    donate_dict = _get_donate_dict()
    donate = donate_dict.get(participant.username, {})
    donate_count = donate.get('count', 0)
    return donate_count


@register.simple_tag
def donated_rank_of_participant(participant):
    donate_dict = _get_donate_dict()
    donate = donate_dict.get(participant.username, {})
    donate_sum = donate.get('sum', 0)

    gt_count = 0
    for key, value in donate_dict.items():
        if donate_sum > value.get('sum', 0):
            gt_count += 1

    if gt_count == 0 and len(donate_dict) == 1:
        top = 100
    else:
        top = gt_count * 100 / (len(donate_dict) if donate_dict else 1)
    return top


@register.filter()
def donate_setting(key='hosting_fees_and_costs'):
    settings = DonateSetting.objects.filter(key=key)
    if settings and len(settings) > 0:
        return settings[0].value
    else:
        return None