from __future__ import division

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from core.decorators import participant_required, scientist_required
from core.utils import json_result, USER_TYPE_SCIENTIST, USER_TYPE_PARTICIPANT
from rating.models import StarRating
from scientist.models import Research, ParticipantResearch, ScientistResearch


@login_required
def get_scientist_score(request):
    return get_score(request, USER_TYPE_SCIENTIST)


@login_required
@participant_required
def set_scientist_score(request):
    return set_score(request, USER_TYPE_SCIENTIST)


@login_required
def get_participant_score(request):
    return get_score(request, USER_TYPE_PARTICIPANT)


@login_required
@scientist_required
def set_participant_score(request):
    return set_score(request, USER_TYPE_PARTICIPANT)


def calc_avg_score(rating_list, type):
    score = 0
    for rating in rating_list:
        if type == 'attitude':
            score += rating.attitude_score
        else:
            score += rating.time_score
    return score / len(rating_list)


def get_score(request, user_type):
    research_id = request.POST.get('research_id', None)
    user_id = request.POST.get('user_id', None)
    type = request.POST.get('type', None)
    score = 0

    try:
        if research_id:
            rating_list = StarRating.objects.filter(to_user__id=user_id, research__id=research_id, user_type=user_type)
        else:
            rating_list = StarRating.objects.filter(to_user__id=user_id, user_type=user_type)

        if rating_list:
            score = calc_avg_score(rating_list, type)
        result = {'status': 'success', 'score': score, 'count': len(rating_list)}
    except Exception as e:
        result = {'status': 'fail', 'reason': e.message}

    return json_result(request, result)


def set_score(request, user_type):
    user_ids = []
    research_id = request.POST.get('research_id', None)
    user_id = request.POST.get('user_id', None)
    score = request.POST.get('score', 0)
    type = request.POST.get('type', None)

    if not user_id:
        participant_ids = request.POST.getlist('participant_id', None)
        scientist_ids = request.POST.getlist('scientist_id', None)
        if participant_ids:
            pr_list = ParticipantResearch.objects.filter(id__in=participant_ids)
            for pr in pr_list:
                user_ids.append(pr.participant.id)
        elif scientist_ids:
            sr_list = ScientistResearch.objects.filter(id__in=participant_ids)
            for sr in sr_list:
                user_ids.append(sr.scientist.id)
    else:
        user_ids.append(user_id)

    try:
        research = Research.objects.get(id=research_id)
        for to_user_id in user_ids:
            rating_list = StarRating.objects.filter(from_user=request.user, to_user__id=to_user_id,
                                                    research__id=research_id,
                                                    user_type=user_type)
            if rating_list:
                rating = rating_list[0]
            else:
                to_user = User.objects.get(id=to_user_id)
                rating = StarRating(from_user=request.user, to_user=to_user, research=research,
                                    user_type=user_type)
            if type == 'attitude':
                rating.attitude_score = score
            else:
                rating.time_score = score
            if not research.is_complete:
                rating.save()
                result = {'status': 'success'}
            else:
                result = {'status': 'fail', 'reason': 'This research has been completed and can not be rating'}
    except Exception as e:
        result = {'status': 'fail', 'reason': e.message}

    return json_result(request, result)