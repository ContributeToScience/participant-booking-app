from department.models import ParticipantCreditScheme
from django.contrib.auth.decorators import login_required
from django.contrib.messages import success, warning
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from haystack.inputs import AutoQuery
from haystack.query import RelatedSearchQuerySet

from core.decorators import participant_required
from core.utils import get_page, json_result
from scientist.models import Research, ParticipantResearch, ScientistResearch, ResearchEvent, ParticipantResearchEvent


@login_required
@participant_required
def participant(request, template='participant/participant.html', extra_context=None):
    context = {}

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@participant_required
def research_list(request, study_type='all', template='participant/research_list.html', extra_context=None):
    if request.method == 'POST':
        q = request.POST.get('q', '')

        research_list = RelatedSearchQuerySet().filter(context=AutoQuery(q)).load_all()

        if study_type == 'ol':
            research_list = research_list.load_all_queryset(Research,
                                                            Research.objects.filter(is_on_web=True, is_publish=True,
                                                                                    is_complete=False).exclude(
                                                                participantresearch__participant=request.user).exclude(
                                                                scientistresearch__scientist=request.user))
        elif study_type == 'nol' or study_type == 'nol_map':
            research_list = research_list.load_all_queryset(Research,
                                                            Research.objects.filter(is_on_web=False, is_publish=True,
                                                                                    is_complete=False).exclude(
                                                                participantresearch__participant=request.user).exclude(
                                                                scientistresearch__scientist=request.user))
        elif study_type == 'all':
            research_list = research_list.load_all_queryset(Research,
                                                            Research.objects.filter(is_publish=True,
                                                                                    is_complete=False).exclude(
                                                                participantresearch__participant=request.user).exclude(
                                                                scientistresearch__scientist=request.user))

        paginator = get_page(request, research_list, 15)

        context = {
            'study_type': study_type,
            'paginator': paginator,
            'research_list': research_list,
            'q': q,
        }
    else:
        research_list = research_randomize(request, study_type)
        paginator = get_page(request, research_list, 15)

        context = {
            'study_type': study_type,
            'paginator': paginator,
            'research_list': research_list,
            'q': '',
        }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


def research_randomize(request, study_type=None):
    if study_type == 'ol':
        research_list = Research.objects.filter(is_publish=True, is_complete=False, is_on_web=True).exclude(
            participantresearch__participant=request.user).exclude(scientistresearch__scientist=request.user)
    elif study_type == 'nol' or study_type == 'nol_map':
        research_list = Research.objects.filter(is_publish=True, is_complete=False, is_on_web=False).exclude(
            participantresearch__participant=request.user).exclude(scientistresearch__scientist=request.user)
    elif study_type == 'all':
        research_list = Research.objects.filter(is_publish=True, is_complete=False).exclude(
            participantresearch__participant=request.user).exclude(scientistresearch__scientist=request.user)
    else:
        research_list = []

    #research_list = filter(lambda x: x.get_distance(request) != 'N/A', research_list)
    research_list = sorted(research_list, key=lambda x: x.get_distance(request))

    return research_list


def research_detail(request, research_id, template='participant/research_detail.html', extra_context=None):
    study_type = request.GET.get('study_type', None)
    scientist_research = get_object_or_404(ScientistResearch, research__id=research_id, research__is_publish=True)
    research = scientist_research.research

    if request.method == 'POST':
        study_type = request.POST.get('study_type', None)
        participant_research_list = ParticipantResearch.objects.filter(participant=request.user, research=research)
        scientist_research = ScientistResearch.objects.filter(scientist=request.user, research=research)

        if participant_research_list:
            if participant_research_list[0].confirmed:
                warning(request, _(u'You are already participants in this research.'))
            else:
                warning(request, _(u'You are already have take part request.'))
        elif scientist_research:
            warning(request, _(u'Can not participate in own research.'))
        else:
            ParticipantResearch(participant=request.user, research=research).save()
            success(request, _(u'Take part request successful.'))
        if research.is_on_web:
            return HttpResponseRedirect(reverse_lazy('research_list', args=[study_type, ]))
        else:
            return HttpResponseRedirect(reverse_lazy('research_list', args=[study_type, ]))

    context = {
        'research': research,
        'study_type': study_type,
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@participant_required
def take_part_researches(request, template='participant/take_part_researches.html', extra_context=None):
    research_list = ParticipantResearch.objects.filter(participant=request.user, confirmed=True)

    context = {
        'research_list': research_list,
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@participant_required
def take_part_researches_calendar(request, template='participant/take_part_researches_calendar.html', extra_context=None):
    research_list = ParticipantResearch.objects.filter(participant=request.user, confirmed=True)

    context = {
        'research_list': research_list,
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@participant_required
def api_participant_events(request):
    research_ids = request.POST.getlist('research_ids', None)
    if research_ids and len(research_ids) > 0:
        research_list = Research.objects.filter(id__in=research_ids, is_publish=True)
    else:
        pr_list = ParticipantResearch.objects.filter(participant=request.user, confirmed=True,
                                                           research__is_publish=True)
        research_list = [pr.research for pr in pr_list]

    event_list = []
    for research in research_list:
        event_list += [event.to_dict() for event in list(research.researchevent_set.all())]

    return json_result(request, event_list)


@login_required
@participant_required
def take_part_event(request):
    event_id = request.POST.get('event_id', None)

    try:
        research_event = get_object_or_404(ResearchEvent, id=event_id)
        participant_event = ParticipantResearchEvent.objects.filter(participant=request.user,
                                                                    research_event=research_event)

        scientist_research = ScientistResearch.objects.filter(scientist=request.user, research=research_event.research)

        if participant_event:
            result = {'status': 'fail', 'reason': 'You have participated in this event'}
        elif scientist_research:
            result = {'status': 'fail', 'reason': 'Can not participate in own research'}
        else:
            ParticipantResearchEvent(participant=request.user,
                                     research_event=research_event).save()
            result = {'status': 'success'}
    except Exception as e:
        result = {'status': 'fail', 'reason': e.message}

    return json_result(request, result)


@login_required
@participant_required
def take_part_credit_schemes(request, template='participant/take_part_credit_schemes.html', extra_context=None):
    credit_scheme_list = ParticipantCreditScheme.objects.filter(participant=request.user)

    context = {
        'credit_scheme_list': credit_scheme_list,
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@participant_required
def payment_messages(request, template='participant/payment_messages.html', extra_context=None):
    if request.method == 'POST':
        participant_id = request.POST.get('participant_id', None)
        participant_resp = request.POST.get('participant_resp', 'false')
        donate_money = request.POST.get('donate_money', 0)

        participant_research = get_object_or_404(ParticipantResearch, id=participant_id, participant=request.user)
        participant_research.participant_resp = False if participant_resp == 'false' else True
        participant_research.donate_credit = float(donate_money) if participant_resp == 'false' else 0
        participant_research.participant_resp_dt = now()
        if participant_research.research.payment_type != 'cash':
            participant_research.save()

    message_list = ParticipantResearch.objects.filter(participant=request.user, confirmed=True, award_credit__gt=0,
                                                      scientist_award_dt__isnull=False, participant_resp__isnull=True,
                                                      participant_resp_dt__isnull=True)

    context = {
        'message_list': message_list,
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@participant_required
def get_payment_info(request):
    participant_id = request.POST.get('participant_id', None)

    try:
        pr = ParticipantResearch.objects.get(id=participant_id)
        result = {
            'status': 'success', 'award_credit': pr.award_credit,
            'research_name': pr.research.name
        }
    except ParticipantResearch.DoesNotExist:
        result = {'status': 'fail', 'reason': 'Participant id is not exist'}

    return json_result(request, result)


    # def send_notification_test(request, type, template='', extra_context=None):
    #     if type == 'scientist':
    #         send_notifications_for_scientists()
    #     else:
    #         send_notifications_for_participants()
    #
    #     context = {}
    #
    #     if extra_context:
    #         context.update(extra_context)
    #     return render_to_response(template, context, context_instance=RequestContext(request))