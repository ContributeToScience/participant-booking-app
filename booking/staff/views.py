import collections
import httplib
import urllib
import urlparse
from django.conf import settings
from django.contrib.messages import error, success, warning
from django.core.urlresolvers import reverse_lazy
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from paypal import PayPalConfig, PayPalInterface, PayPalAPIResponseError

from core.decorators import staff_required
from scientist.models import ParticipantResearch, Research


@staff_required
def award_participants(request, template='staff/award_participants.html', extra_context=None):
    """
    Staff user: award to participants page

    **Context**

    ``RequestContext``

    **Template:**

    :template:`staff/award_participants.html`

    """

    payment_paypal_dict = {}
    payment_amazon_dict = {}
    payment_type = None

    if request.method == 'POST':
        payment_type = request.POST.get('payment_type', None)
        paypal_type = request.POST.get('paypal_type', None)
        award_participant_id_list = request.POST.getlist('award_participant_id', [])
        _participant_group_by_payment_type(request, award_participant_id_list, payment_paypal_dict, payment_amazon_dict)
        redirect_url = _payment_of_paypal(request, payment_paypal_dict, paypal_type)
        if redirect_url:
            return HttpResponseRedirect(redirect_url)
        _payment_of_amazon(request, payment_amazon_dict)

    award_participant_list = ParticipantResearch.objects.filter(confirmed=True, award_credit__gt=0,
                                                                scientist_award_dt__isnull=False,
                                                                participant_resp_dt__isnull=False,
                                                                superuser_award_dt__isnull=True).filter(
        award_credit__gt=F('donate_credit')).order_by('-created')

    if payment_type:
        _participant_group_by_payment_type(request, award_participant_list, payment_paypal_dict, payment_amazon_dict,
                                           False)

    if payment_type == 'paypal':
        award_participant_list = payment_paypal_dict.values()
    elif payment_type == 'amazon':
        award_participant_list = payment_amazon_dict.values()

    context = {
        'award_participant_list': award_participant_list,
        'payment_type': payment_type
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


def _participant_group_by_payment_type(request, participant_list, payment_paypal_dict, payment_amazon_dict,
                                       search=True):
    if participant_list and len(participant_list) > 0:
        for item in participant_list:
            if search:
                participant = ParticipantResearch.objects.get(id=item)
            else:
                participant = item
            user_profile = participant.participant.userprofile
            participant_info = user_profile.basic_info.get('participant', None)
            payment_type = participant_info.get('payment_type', None) if participant_info else None
            payment_account = participant_info.get('payment_account', None) if participant_info else None

            if payment_type == 'paypal':
                payment_paypal_dict['%s_%s' % (payment_account, participant.id)] = participant
            elif payment_type == 'amazon':
                payment_amazon_dict['%s_%s' % (payment_account, participant.id)] = participant
            else:
                username = user_profile.get_full_name()
                warning(request, _(u'Please check %s user profile whether to fill in payment information' % username))


def _payment_of_paypal(request, payment_paypal_dict, paypal_type):
    if payment_paypal_dict and len(payment_paypal_dict) > 0:
        if paypal_type == 'MassPay':
            _mass_pay(request, payment_paypal_dict)
        elif paypal_type == 'AdaptivePay':
            return _adaptive_pay(request, payment_paypal_dict)
        else:
            error(request, _(u'Please choose a payment method in MassPay or AdaptivePay'))


def _payment_of_amazon(request, payment_amazon_dict):
    #TODO: Amazon payment method
    print payment_amazon_dict
    pass


def _mass_pay(request, payment_paypal_dict):
    PAYPAL_CONFIG = PayPalConfig(API_USERNAME=settings.PAYPAL_API_USERNAME,
                                 API_PASSWORD=settings.PAYPAL_API_PASSWORD,
                                 API_SIGNATURE=settings.PAYPAL_API_SIGNATURE,
                                 API_ENVIRONMENT=settings.PAYPAL_API_ENVIRONMENT,
                                 DEBUG_LEVEL=0)
    paypal_interface = PayPalInterface(config=PAYPAL_CONFIG)
    payment_dict = {'RECEIVERTYPE': 'EmailAddress', }

    for i, item in enumerate(payment_paypal_dict.items()):
        payment_account = (item[0])[0:item[0].find('_')]
        participant = item[1]
        payment_credit = participant.award_credit - participant.donate_credit
        if payment_credit > 0:
            if payment_account:
                payment_dict['L_EMAIL%s' % i] = payment_account
                payment_dict['L_AMT%s' % i] = payment_credit
                payment_dict['L_NOTE%s' % i] = participant.research.name
                participant.superuser_award_dt = now()
                participant.payment_type = 'paypal'
                participant.payment_account = payment_account

    try:
        resp = paypal_interface._call('MassPay', **payment_dict)
        if resp['ACK'] == 'Success':
            for payment_account, participant in payment_paypal_dict.items():
                participant.payment_status = True
                participant.payment_resp = 'MassPay Success'
                participant.save()
            success(request, _(u'Payment of payment successful'))
    except PayPalAPIResponseError as e:
        error(request, _(u'%s') % e.message)


def _adaptive_pay(request, payment_paypal_dict):
    #Set headers
    headers = {
        'X-PAYPAL-SECURITY-USERID': settings.PAYPAL_API_USERNAME,
        'X-PAYPAL-SECURITY-PASSWORD': settings.PAYPAL_API_PASSWORD,
        'X-PAYPAL-SECURITY-SIGNATURE': settings.PAYPAL_API_SIGNATURE,
        'X-PAYPAL-APPLICATION-ID': settings.PAYPAL_APPLICTION_ID,
        'X-PAYPAL-SERVICE-VERSION': '1.1.0',
        'X-PAYPAL-REQUEST-DATA-FORMAT': 'NV',
        'X-PAYPAL-RESPONSE-DATA-FORMAT': 'NV'
    }

    #Set POST Parameters
    params = collections.OrderedDict()
    params['requestEnvelope.errorLanguage'] = 'en_US'
    params['requestEnvelope.detailLevel'] = 'ReturnAll'
    params['reverseAllParallelPaymentsOnError'] = 'true'
    params['actionType'] = 'PAY'
    params['currencyCode'] = 'USD'
    params['feesPayer'] = 'EACHRECEIVER'

    payment_params = '?type=AdaptivePay'
    for i, item in enumerate(payment_paypal_dict.items()):
        payment_account = (item[0])[0:item[0].find('_')]
        participant = item[1]
        payment_params += '&pr=%s' % item[0]
        payment_credit = participant.award_credit - participant.donate_credit
        if payment_credit > 0:
            if payment_account:
                params['receiverList.receiver(%d).email' % i] = payment_account
                params['receiverList.receiver(%d).amount' % i] = payment_credit

    params['returnUrl'] = '%s/staff/payment/paypal/complete/%s' % (settings.SITE_NAME, payment_params)
    params['cancelUrl'] = '%s%s' % (settings.SITE_NAME, request.path)
    #params['returnUrl'] = 'http://www.baidu.com
    #params['cancelUrl'] = 'http://www.baidu.com

    #Set Client Details
    params['clientDetails.ipAddress'] = '127.0.0.1'
    params['clientDetails.deviceId'] = 'mydevice'
    params['clientDetails.applicationId'] = 'PayNvpDemo'

    enc_params = urllib.urlencode(params)

    #Connect to sand box and POST.
    conn = httplib.HTTPSConnection(settings.PAYPAL_SERVICE)
    conn.request("POST", "/AdaptivePayments/Pay/", enc_params, headers)

    #Check the response - should be 200 OK.
    response = conn.getresponse()

    if response.status == 200:
        #Get the reply and print it out.
        data = response.read()
        result = urlparse.parse_qs(data)
        if result['responseEnvelope.ack'][0] == 'Success':
            return '%s?cmd=_ap-payment&paykey=%s' % (settings.PAYPAL_ACTION, result['payKey'][0])
        else:
            error(request, _(u'%s' % result['error(0).message'][0]))
    else:
        warning(request, _(u'Request an exception, please try again later'))


@require_GET
@csrf_exempt
def payment_paypal_complete(request):
    pr_list = request.GET.getlist('pr', [])
    #payment_type = request.GET.get('type', '')

    try:
        for pr in pr_list:
            payment_account = pr[0:pr.find('_')]
            pr_id = pr[pr.find('_') + 1:len(pr)]
            pr = ParticipantResearch.objects.get(id=pr_id)
            pr.superuser_award_dt = now()
            pr.payment_type = 'paypal'
            pr.payment_account = payment_account
            pr.payment_status = True
            pr.payment_resp = 'AdaptivePay Success'
            pr.save()
    except Exception as e:
        error(request, _(u'%s' % e.message))
    return HttpResponseRedirect(reverse_lazy('award_participants'))


@staff_required
def award_participants_history(request, template='staff/award_participants_history.html', extra_context=None):
    """
    Staff user: award to participants history page

    **Context**

    ``RequestContext``

    **Template:**

    :template:`staff/award_participants_history.html`

    """

    award_participant_history_list = ParticipantResearch.objects.filter(confirmed=True, award_credit__gt=0,
                                                                        scientist_award_dt__isnull=False,
                                                                        participant_resp_dt__isnull=False,
                                                                        superuser_award_dt__isnull=False).order_by(
        '-created')

    context = {
        'award_participant_history_list': award_participant_history_list,
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@staff_required
def scientists_payment_history(request, template='staff/scientists_payment_history.html', extra_context=None):
    """
    Staff user: scientists payment history page

    **Context**

    ``RequestContext``

    **Template:**

    :template:`staff/scientists_payment_history.html`

    """

    scientist_payment_history_list = Research.objects.filter(is_paid=True).order_by('-created')

    context = {
        'scientist_payment_history_list': scientist_payment_history_list,
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))