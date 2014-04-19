import datetime
import json
from dateutil import parser

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.messages import success, error, warning
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from paypal.standard.forms import PayPalPaymentsForm

from core.decorators import scientist_required
from core.utils import json_result, get_location, is_float, is_integer

from .models import Research, ScientistResearch, ParticipantResearch, ResearchEvent, ParticipantResearchEvent, LocationInfo, RemindScientistInfo, RemindParticipantInfo, ScientistPaymentRecord, AnonymousDonateRecord
from department.models import ScientistCreditScheme, ParticipantCreditScheme, CreditScheme, SchemeCreditRecord
from .forms import ResearchForm

@login_required
@scientist_required
def scientist(request, template='scientist/scientist.html', extra_context=None):
    """
    Scientist homepage, login required.

    **Context**

    ``RequestContext``

    **Template:**

    :template:`scientist/home.html`

    """
    context = {
    }
    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def scientist_research_post(request, research_id=None, template='scientist/research_post.html', extra_context=None):
    """
    Scientist create/edit research page, login required.

    **Context**

    ``RequestContext``

    **Template:**

    :template:`scientist/research_post.html`

    """
    type = request.POST.get('type', 'edit')
    return get_research_form(request, research_id, type, template, extra_context)


@login_required
@scientist_required
def scientist_research_list(request, template='scientist/research_list.html', extra_context=None):
    """
    Scientist list research page, login required.
    This page will use backbonejs to call restful api to show data.

    **Context**

    ``RequestContext``

    **Template:**

    :template:`scientist/research_list.html`

    """

    research_list = Research.objects.filter(scientistresearch__scientist=request.user).order_by('-created')

    context = {
        'research_list': research_list
    }
    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@scientist_required
def update_publish_status(request):
    research_id = request.POST.get('research_id', None)
    is_publish = request.POST.get('is_publish', 'false')
    if research_id:
        research = Research.objects.get(id=research_id)

        if is_publish == 'true':
            research.is_publish = True
        else:
            research.is_publish = False
        research.save()

        # If the research is not paid, redirect to payment page
        if research.is_publish and research.total_credit > 0 and research.is_paid is False:
            research.is_publish = False
            if research.payment_type == 'cash':
                research.is_paid = True
                research.save()
            else:
                research.save()
                if research.payment_type == 'paypal':
                    result = {'status': 'warning',
                              'redirect_url': '/scientist/research/%s/payment/paypal/' % research.id}
                elif research.payment_type == 'amazon':
                    result = {'status': 'warning',
                              'redirect_url': '/scientist/research/%s/payment/amazon/' % research.id}
        else:
            result = {'status': 'success'}
    else:
        result = {'status': 'fail', 'reason': 'Research id is none'}
    return json_result(request, result)


@login_required
@scientist_required
def research_copy(request, research_id=None, template='scientist/research_post.html', extra_context=None):
    return get_research_form(request, research_id, 'copy', template, extra_context)


def get_research_form(request, research_id, type='edit', template='scientist/research_post.html', extra_context=None):
    research = None
    is_paid = False
    total_credit = 0

    if research_id:
        research = get_object_or_404(Research, id=research_id, scientistresearch__scientist=request.user)
        total_credit = research.total_credit
        if type == 'edit':
            is_paid = research.is_paid
            if research.is_complete:
                return HttpResponseRedirect(reverse_lazy('scientist_research_list'))

    if request.method == 'POST':
        form = ResearchForm(data=request.POST, files=request.FILES, instance=research)
        if form.is_valid():
            research = form.save(commit=False)

            address = form.cleaned_data['address']
            lng = form.cleaned_data['lng']
            lat = form.cleaned_data['lat']

            if address and lng > 0 and lat > 0:
                location_info = LocationInfo(address=address, lng=lng, lat=lat)
                location_info.save()
                research.location = location_info

            remind_scientist_info = json.loads(form.cleaned_data['remind_scientist_info'])

            if remind_scientist_info and len(remind_scientist_info) > 0:
                RemindScientistInfo.objects.filter(research=research).delete()

                for remind_scientist in remind_scientist_info:
                    message_type = remind_scientist['type']
                    time = remind_scientist['time']
                    time_type = remind_scientist['time_type']
                    message = remind_scientist['message']
                    RemindScientistInfo(research=research, type=message_type, time=time, time_type=time_type,
                                        message=message).save()

            remind_participant_info = json.loads(form.cleaned_data['remind_participant_info'])

            if remind_participant_info and len(remind_participant_info) > 0:
                RemindParticipantInfo.objects.filter(research=research).delete()

                for remind_participant in remind_participant_info:
                    message_type = remind_participant['type']
                    time = remind_participant['time']
                    time_type = remind_participant['time_type']
                    message = remind_participant['message']
                    RemindParticipantInfo(research=research, type=message_type, time=time, time_type=time_type,
                                          message=message).save()

            if type == 'edit':
                research.is_publish = True
            elif type == 'draft':
                research.is_publish = False
            elif type == 'copy':
                research.id = None
                research.is_paid = False
                research.is_complete = False
                research.payment_dt = None
                research.created = now()

            if is_paid:
                research.total_credit = total_credit

            research.save()

            scientist_research = ScientistResearch.objects.filter(scientist=request.user, research=research)
            if not scientist_research:
                ScientistResearch(scientist=request.user, research=research).save()

            # If the research is not paid, redirect to payment page
            if research.is_publish and research.total_credit > 0 and research.is_paid is False:
                userprofile = request.user.userprofile
                userprofile.available_balance -= research.total_credit

                if research.payment_type == 'cash':
                    research.is_paid = True
                    research.save()
                elif userprofile.available_balance >= 0:
                    research.is_paid = True
                    research.save()
                    userprofile.save()
                    ScientistPaymentRecord(scientist=request.user, credit=-research.total_credit,
                                           description='payment for [id=%s, name=%s] research' % (
                                               research.id, research.name)).save()
                else:
                    research.is_publish = False
                    research.save()
                    if research.payment_type == 'paypal':
                        return HttpResponseRedirect(
                            reverse_lazy('scientist_research_payment_paypal', args=[research.id, ]))
                    elif research.payment_type == 'amazon':
                        return HttpResponseRedirect(
                            reverse_lazy('scientist_research_payment_amazon', args=[research.id, ]))
                    elif research.payment_type == 'fake':
                        return HttpResponseRedirect(
                            reverse_lazy('scientist_research_payment_fake', args=[research.id, ]))
            return HttpResponseRedirect(reverse_lazy('scientist_research_list'))
    else:
        location = get_location(request)

        if research:
            form = ResearchForm(instance=research, initial={
                'address': research.location.address if research.location else '',
                'lng': research.location.lng if research.location else location['lng'],
                'lat': research.location.lat if research.location else location['lat'],
            })
        else:
            form = ResearchForm(initial={
                'address': '',
                'lng': location['lng'],
                'lat': location['lat'],
            })

    context = {
        'form': form,
        'type': type,
        'research_id': research_id,
        'is_paid': is_paid,
        'remind_scientist_info': research.remindscientistinfo_set.all() if research else None,
        'remind_participant_info': research.remindparticipantinfo_set.all() if research else None,
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@scientist_required
def research_delete(request):
    research_id = request.POST.get('research_id', None)
    if research_id:
        Research.objects.get(id=research_id).delete()
        result = {'status': 'success'}
    else:
        result = {'status': 'fail', 'reason': 'research id is none'}
    return json_result(request, result)


@login_required
@scientist_required
def research_detail(request, research_id, template='scientist/research_detail.html', extra_context=None):
    """
    Scientist research detail page, login required.

    **Context**

    ``RequestContext``

    **Template:**

    :template:`scientist/research_detail.html`

    """
    research = get_object_or_404(Research, id=research_id, scientistresearch__scientist=request.user)
    participant_list = ParticipantResearch.objects.filter(research=research).order_by('-created')

    context = {
        'research': research,
        'participant_list': participant_list,
    }
    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@scientist_required
def confirmed_participant(request):
    research_id = request.POST.get('research_id', None)
    if research_id:
        research = get_object_or_404(Research, id=research_id)
        if not research.is_complete:
            participant_id_list = request.POST.getlist('participant_id', [])
            for participant_id in participant_id_list:
                participant_research = ParticipantResearch.objects.filter(id=participant_id, research=research,
                                                                          confirmed=False)
                if participant_research:
                    participant_research[0].confirmed = True
                    participant_research[0].save()
            result = {'status': 'success'}
    else:
        result = {'status': 'fail', 'reason': 'Research id is none'}
    return json_result(request, result)


@login_required
@scientist_required
def reject_participant(request):
    research_id = request.POST.get('research_id', None)
    if research_id:
        count = 0
        research = get_object_or_404(Research, id=research_id)
        if not research.is_complete:
            participant_id_list = request.POST.getlist('participant_id', [])
            for participant_id in participant_id_list:
                participant_research = ParticipantResearch.objects.filter(id=participant_id, research=research,
                                                                          confirmed=False)
                if participant_research:
                    participant_research[0].delete()
                    count += 1
            if count > 0:
                result = {'status': 'success'}
            else:
                result = {'status': 'warn', 'reason': 'You can not reject already confirmed participant'}
    else:
        result = {'status': 'fail', 'reason': 'Research id is none'}
    return json_result(request, result)


@login_required
@scientist_required
def assign_credit(request, template='scientist/assign_credit.html', extra_context=None):
    research_id = request.REQUEST.get('research_id', None)
    participant_id_list = request.REQUEST.getlist('participant_id')

    research = get_object_or_404(Research, id=research_id, scientistresearch__scientist=request.user)

    if not research.is_paid:
        return HttpResponseRedirect(reverse_lazy('research_detail', args=[research.id]))

    participant_list = []
    for participant_id in participant_id_list:
        participant = ParticipantResearch.objects.filter(id=participant_id, research=research, confirmed=True,
                                                         award_credit=0, scientist_award_dt__isnull=True)
        if participant and len(participant) > 0:
            participant_list.append(participant[0])

    if not participant_list or len(participant_list) <= 0:
        warning(request, _(u'Please confirm participant before assign credit'))
        return HttpResponseRedirect(reverse_lazy('research_detail', args=[research.id]))

    if request.method == 'POST':
        assign_credit = request.POST.get('assign_credit', 0)
        assign_credit = is_float(assign_credit, True)
        if assign_credit <= 0:
            warning(request, _(u'Assign credit should be greater than 0'))
        elif (assign_credit * len(participant_list)) > research.total_credit:
            error(request, _(u'Not enough total credit'))
        else:
            for participant in participant_list:
                participant.award_credit += assign_credit
                participant.scientist_award_dt = now()
                participant.save()
            success(request, _(u'Assign credit succeed'))
            return HttpResponseRedirect(reverse_lazy('research_detail', args=[research.id]))

    context = {
        'research': research,
        'participant_list': participant_list,
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@scientist_required
def scientist_scheme_list(request, template='scientist/scheme_list.html', extra_context=None):
    context = {
        'scheme_list': ScientistCreditScheme.objects.filter(scientist=request.user),
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@scientist_required
def scientist_scheme_detail(request, scheme_id, template='scientist/scheme_detail.html', extra_context=None):
    scheme = get_object_or_404(ScientistCreditScheme, id=scheme_id, scientist=request.user)

    context = {
        'scheme': scheme,
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@scientist_required
def scheme_assign_credit(request):
    try:
        scheme_id = request.POST.get('scheme_id', None)
        participant_id = request.POST.get('participant_id', None)
        assigned_credit = is_integer(request.POST.get('assigned_credit', 0))

        scheme = get_object_or_404(CreditScheme, id=scheme_id)
        scientist = get_object_or_404(ScientistCreditScheme, credit_scheme=scheme, scientist=request.user)
        participant = get_object_or_404(ParticipantCreditScheme, id=participant_id, credit_scheme=scheme)

        if assigned_credit < 0:
            result = {'status': 'fail', 'reason': 'remain credit can not assign to negative number'}
        elif assigned_credit > scientist.remain_credit:
            result = {'status': 'fail', 'reason': 'not enough remain credit'}
        else:
            scientist.remain_credit -= assigned_credit
            scientist.save()
            participant.incomplete_credit -= assigned_credit
            participant.save()
            SchemeCreditRecord(credit_scheme=scheme, scientist=scientist.scientist,
                               participant=participant.participant).save()
            result = {'status': 'success', 'scientist_remain_credit': scientist.remain_credit,
                      'participant_incomplete_credit': participant.incomplete_credit}
    except Exception as e:
        result = {'status': 'fail', 'reason': e.message}
    return json_result(request, result)


@login_required
@scientist_required
def api_scientist_events(request):
    research_id = request.REQUEST.get('research_id', None)
    if research_id:
        research_list = ScientistResearch.objects.filter(research__id=research_id, scientist=request.user)
    else:
        research_list = ScientistResearch.objects.filter(scientist=request.user)
    event_list = []
    for research in research_list:
        event_list += [event.to_dict() for event in list(research.research.researchevent_set.all())]

    return json_result(request, event_list)


@login_required
@scientist_required
def research_event_list(request, research_id, template='scientist/research_event_list.html', extra_context=None):
    research = Research.objects.get(id=research_id)
    if research.is_complete:
        return HttpResponseRedirect(reverse_lazy('scientist_research_list'))
    else:
        context = {
            'research': research
        }

        if extra_context:
            context.update(extra_context)
        return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@scientist_required
def create_research_event(request):
    research_id = request.POST.get('research_id', None)
    start = request.POST.get('start', None)
    end = request.POST.get('end', None)
    event_id = request.POST.get('event_id', None)

    research = get_object_or_404(Research, id=research_id)
    is_validate = True

    start = start.replace('GMT', '')
    end = end.replace('GMT', '')
    d_start = parser.parse(start).replace(tzinfo=None)
    d_end = parser.parse(end).replace(tzinfo=None)

    if d_start > d_end:
        result = {'status': 'fail', 'reason': 'event end time can not be greater than the start time',
                  'target': 'id_end'}
        is_validate = False
    elif research.start > d_start:
        result = {'status': 'fail', 'reason': 'event start time can not before the start time of research',
                  'target': 'id_start'}
        is_validate = False
    elif d_end > research.end:
        result = {'status': 'fail', 'reason': 'event end time can not after the end time of research',
                  'target': 'id_end'}
        is_validate = False

    if is_validate:
        try:
            if event_id:
                event = ResearchEvent.objects.get(id=event_id)
                event.start = d_start
                event.end = d_end
                event.save()
            else:
                ResearchEvent(research=research, start=d_start, end=d_end).save()
            result = {'status': 'success'}
        except Exception as e:
            result = {'status': 'fail', 'reason': e.message}

    return json_result(request, result)


@login_required
@scientist_required
def delete_research_event(request):
    event_id = request.POST.get('event_id', None)

    if event_id:
        try:
            event = ResearchEvent.objects.get(id=event_id)
            participant_event_list = ParticipantResearchEvent.objects.filter(research_event=event)
            if len(participant_event_list) > 0:
                result = {'status': 'fail', 'reason': 'event has been participants'}
            else:
                participant_event_list.delete()
                event.delete()
                result = {'status': 'success'}
        except ResearchEvent.DoesNotExist:
            result = {'status': 'fail', 'reason': 'event does not exist'}
    else:
        result = {'status': 'fail', 'reason': 'event does not exist'}

    return json_result(request, result)


@login_required
@scientist_required
def copy_research_event(request):
    event_id = request.POST.get('event_id', None)
    start = request.POST.get('start', None)
    research_id = request.POST.get('research_id', None)

    research = get_object_or_404(Research, id=research_id)
    is_validate = True

    if event_id and start:
        try:
            event = ResearchEvent.objects.get(id=event_id)
            event.id = None
            seconds = (event.end - event.start).seconds
            days = (event.end - event.start).days
            start = start.replace('GMT', '')
            d_start = parser.parse(start).replace(tzinfo=None)

            event.end = d_start + datetime.timedelta(days=days, seconds=seconds)
            event.start = d_start

            if research.start > d_start:
                result = {'status': 'fail', 'reason': 'event start time can not before the start time of research',
                          'target': 'id_start'}
                is_validate = False
            elif research.end < event.end:
                result = {'status': 'fail', 'reason': 'event end time can not after the end time of research',
                          'target': 'id_end'}
                is_validate = False

            if is_validate:
                event.save()
                result = {'status': 'success'}
        except ResearchEvent.DoesNotExis:
            result = {'status': 'fail', 'reason': 'event does not exist'}
    else:
        result = {'status': 'fail', 'reason': 'event does not exist'}

    return json_result(request, result)


@login_required
@scientist_required
def get_research_event(request):
    event_id = request.POST.get('event_id', None)

    if event_id:
        event = ResearchEvent.objects.get(id=event_id)
        result = {'status': 'success', 'event': event.to_dict()}
    else:
        result = {'status': 'fail', 'reason': 'event does not exist'}

    return json_result(request, result)


@login_required
@scientist_required
def event_participant_list(request, event_id, template='scientist/event_participant_list.html', extra_context=None):
    research_event = get_object_or_404(ResearchEvent, id=event_id)
    scientist_research = get_object_or_404(ScientistResearch, research=research_event.research)
    if request.user == scientist_research.scientist:
        participant_list = research_event.participantresearchevent_set.all()
    else:
        participant_list = None

    context = {
        'research': research_event.research,
        'participant_list': participant_list,
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@scientist_required
def resize_research_event(request):
    research_id = request.POST.get('research_id', None)
    event_id = request.POST.get('event_id', None)
    start_delta = request.POST.get('start_delta', None)
    end_delta = request.POST.get('end_delta', None)

    try:
        research = get_object_or_404(Research, id=research_id)
        event = get_object_or_404(ResearchEvent, id=event_id)
        if start_delta:
            event.start += datetime.timedelta(minutes=is_integer(start_delta))
        if end_delta:
            event.end += datetime.timedelta(minutes=is_integer(end_delta))
        if research.start > event.start:
            result = {'status': 'fail', 'reason': 'event start time can not before the start time of research'}
        elif research.end < event.end:
            result = {'status': 'fail', 'reason': 'event end time can not after the end time of research'}
        else:
            event.save()
            result = {'status': 'success'}
    except Exception as e:
        result = {'status': 'fail', 'reason': e.message}

    return json_result(request, result)


@login_required
@scientist_required
def scientist_research_payment_fake(request, research_id, template='scientist/research_payment_fake.html',
                                    extra_context=None):
    if request.method == 'POST':
        sr = get_object_or_404(ScientistResearch, research__id=int(request.POST.get('research_id')))
        research = sr.research
        research.is_paid = True
        research.is_publish = True
        research.payment_dt = now()
        research.save()

        userprofile = sr.scientist.userprofile

        ScientistPaymentRecord(scientist=sr.scientist, credit=research.total_credit - userprofile.available_balance,
                               description='recharge to account').save()

        remark = ''
        if userprofile.available_balance > 0:
            remark = ',using the balance of payment %s' % userprofile.available_balance
            userprofile.available_balance = 0
            userprofile.save()

        ScientistPaymentRecord(scientist=sr.scientist, credit=-research.total_credit,
                               description='payment for [id=%s, name=%s] research%s' % (
                                   research.id, research.name, remark)).save()

        return HttpResponseRedirect(reverse_lazy('research_detail', args=[research.id]))
    else:
        research = get_object_or_404(Research, id=research_id, scientistresearch__scientist=request.user)

        context = {
            'research': research,
            'amount': research.total_credit - request.user.userprofile.available_balance,
        }

        if extra_context:
            context.update(extra_context)

        return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@scientist_required
def scientist_research_payment_paypal(request, research_id, template='scientist/research_payment_paypal.html',
                                      extra_context=None):
    research = get_object_or_404(Research, id=research_id, scientistresearch__scientist=request.user)

    # What you want the button to do.
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': research.total_credit - request.user.userprofile.available_balance,
        'item_name': research.name,
        'invoice': '%s-%d' % (research.name, research.id),
        'notify_url': '%s%s' % (settings.SITE_NAME, reverse_lazy('paypal-ipn')),
        'return_url': '%s%s' % (settings.SITE_NAME, reverse_lazy('research_paypal_complete', args=[research.id, ])),
        'cancel_return': 'http://www.example.com/your-cancel-location/',
        'custom': research.id,
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    if settings.PAYPAL_API_ENVIRONMENT == 'SANDBOX':
        paypal_form = form.sandbox()
    else:
        paypal_form = form.render()

    context = {
        'form': paypal_form,
        'research': research,
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@require_POST
@csrf_exempt
def research_paypal_complete(request, research_id):
    sr = get_object_or_404(ScientistResearch, research__id=int(request.REQUEST.get('custom')))
    research = sr.research
    research.is_paid = True
    research.is_publish = True
    research.payment_dt = now()
    research.save()

    userprofile = sr.scientist.userprofile

    ScientistPaymentRecord(scientist=sr.scientist, credit=research.total_credit - userprofile.available_balance,
                           description='recharge to account').save()

    remark = ''
    if userprofile.available_balance > 0:
        remark = ',using the balance of payment %s' % userprofile.available_balance
        userprofile.available_balance = 0
        userprofile.save()

    ScientistPaymentRecord(scientist=sr.scientist, credit=-research.total_credit,
                           description='payment for [id=%s, name=%s] research%s' % (
                           research.id, research.name, remark)).save()

    return HttpResponseRedirect(reverse_lazy('research_detail', args=[research.id]))


@login_required
@scientist_required
def scientist_research_payment_amazon(request, research_id, template='scientist/research_payment_amazon.html',
                                      extra_context=None):
    research = get_object_or_404(Research, id=research_id, scientistresearch__scientist=request.user)

    #TODO Amazon payment stuff

    context = {
        'research': research,
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@scientist_required
def update_research_duration(request):
    research_id = request.POST.get('research_id', None)
    start = request.POST.get('start', None)
    end = request.POST.get('end', None)

    try:
        research = Research.objects.get(id=research_id)
        research.start = start
        research.end = end
        research.save()
        result = {'status': 'success'}
    except Exception as e:
        result = {'status': 'fail', 'reason': e.message}

    return json_result(request, result)


@login_required
@scientist_required
def update_complete_status(request, research_id):
    try:
        sr = ScientistResearch.objects.get(research__id=research_id, scientist=request.user)
        research = sr.research
        if not research.is_complete:
            research.is_complete = True
            research.save()
            if research.is_paid and research.payment_type != 'cash':
                userprofile = request.user.userprofile
                userprofile.available_balance += research.remain_credit
                userprofile.save()
                ScientistPaymentRecord(scientist=sr.scientist, credit=research.remain_credit,
                                       description='refund from [id=%s, name=%s] research' % (
                                       research.id, research.name)).save()
    except Exception as e:
        error(request, e.message)

    return HttpResponseRedirect(reverse_lazy('scientist_research_list'))


@login_required
@scientist_required
def scientist_payment_record(request, template='scientist/payment_record.html', extra_context=None):
    record_list = ScientistPaymentRecord.objects.filter(scientist=request.user)

    context = {
        'record_list': record_list,
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@require_POST
@csrf_exempt
def anonymous_donate_paypal_complete(request):
    first_name = request.POST.get('first_name', None)
    last_name = request.POST.get('last_name', None)
    payer_email = request.POST.get('payer_email', None)
    donate_amount = request.POST.get('payment_gross', 0)
    AnonymousDonateRecord(first_name=first_name, last_name=last_name, email=payer_email,
                          donate_amount=donate_amount).save()
    return HttpResponseRedirect(reverse_lazy('home'))