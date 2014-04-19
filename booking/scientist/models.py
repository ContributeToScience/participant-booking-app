import math
import datetime
from message.models import Message
from message.utils import TYPE_FEEDBACK
from model_utils.models import TimeStampedModel

from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from categories.models import CategoryBase
from paypal.standard.ipn.signals import payment_was_successful

CURRENCY_CHOICES = (
    ('$', '$ US Dollor'),
)

PAYMENT_TYPE_CHOICES = (
    ('cash', _(u'Cash')),
    ('paypal', _(u'PayPal')),
    #('amazon', _(u'Amazon')),
    ('fake', _(u'Keep track of money only')),
)

FEEDBACK_STATUS_PENDING = 0
FEEDBACK_STATUS_SEND_REMIND = 1
FEEDBACK_STATUS_PUNISHMENT = 2

FEEDBACK_STATUS_CHOICES = (
    (FEEDBACK_STATUS_PENDING, _(u'Pending')),
    (FEEDBACK_STATUS_SEND_REMIND, _(u'Send Remind')),
    (FEEDBACK_STATUS_PUNISHMENT, _(u'Punishment')),
)


class Category(CategoryBase):
    pass


class LocationInfo(TimeStampedModel):
    address = models.CharField(verbose_name=_(u'Address'), max_length=255, null=False, blank=False, default='')
    lng = models.FloatField(verbose_name=_(u'Longitude'), null=False, blank=False, default=0)
    lat = models.FloatField(verbose_name=_(u'Latitude'), null=False, blank=False, default=0)


class Research(TimeStampedModel):
    '''
    This model store the study (or researcher) information
    '''
    #researcher = models.ForeignKey(User, verbose_name=_(u'Researcher'))
    name = models.CharField(verbose_name=_(u'Research Name'), max_length=100)
    description = models.TextField(verbose_name=_(u'Description'), max_length=1024, null=True, blank=True)
    need_participant_num = models.PositiveIntegerField(verbose_name=_(u'Number of participants needed'))
    is_on_web = models.BooleanField(verbose_name=_(u'Is on web or not?'), default=False)
    location = models.ForeignKey(LocationInfo, verbose_name=_(u'Location'), null=True, blank=True)
    room = models.CharField(verbose_name=_(u'Room'), max_length=255, null=True, blank=True)
    url = models.URLField(verbose_name=_(u'Web URL'), max_length=255, null=True, blank=True)
    start = models.DateTimeField(verbose_name=_(u'Start time'))
    end = models.DateTimeField(verbose_name=_(u'End time'))
    #duration = models.CharField(verbose_name=_(u'Duration'), max_length=255)
    remuneration = models.PositiveIntegerField(verbose_name=_(u'Remuneration'), null=True, blank=True, default=0)
    currency = models.CharField(verbose_name=_(u'Currency'), choices=CURRENCY_CHOICES, default='$', max_length=1)
    ethical_permission = models.BooleanField(verbose_name=_(u'Ethical permission to do study'), default=False)
    non_ethical_permission_reason = models.CharField(_(u'I do not need ethical permission to do this study reason'),
                                                     max_length=255, null=True, blank=True)
    further_ethical_permisson_info = models.CharField(verbose_name=_(u'Further Ethical permission info'),
                                                      max_length=255, null=True, blank=True)
    restrictions = models.CharField(verbose_name=_(u'Restrictions'), max_length=255, null=True, blank=True)
    # Remind the researcher
    remind_research = models.BooleanField(verbose_name=_(u'Send experimenter reminder emails'), default=False)
    # Remind the participants
    remind_participant = models.BooleanField(verbose_name=_(u'Send participants reminder emails'), default=False)
    is_publish = models.BooleanField(verbose_name=_(u'Is publish?'))
    total_credit = models.FloatField(null=True, blank=True, default=0)
    is_anonymous = models.BooleanField(verbose_name=_(u'Do people who sign up for your study need to remain anonymous to you until you conduct the research?'), default=False)
    is_credit_scheme = models.BooleanField(verbose_name=_(u'Is this study done within a participant credit scheme?'),
                                           default=False)
    payment_type = models.CharField(null=True, blank=True, choices=PAYMENT_TYPE_CHOICES, max_length=10)
    is_paid = models.BooleanField(verbose_name=_(u'Is the study has been paid for publish?'), default=False)
    payment_dt = models.DateTimeField(verbose_name=_(u'Payment datetime'), null=True, blank=True)
    default_event_duration = models.PositiveIntegerField(verbose_name=_(u'Time/Experiment'), null=True, blank=True,
                                                         default=45)
    is_complete = models.BooleanField(verbose_name=_(u'Is the study has been complete?'), default=False)
    is_feedback_promise = models.BooleanField(verbose_name=_(u'I will provide feedback to my participants about the results of the experiment and whether or not the research was published'), default=False)
    feedback_promise_time = models.DateTimeField(verbose_name=_(u'Feedback promise time'), null=True, blank=True)
    non_feedback_reason = models.CharField(verbose_name=_(u'Non feedback reason'), max_length=255, null=True, blank=True)
    feedback_status = models.IntegerField(choices=FEEDBACK_STATUS_CHOICES, default=FEEDBACK_STATUS_PENDING, verbose_name=_(u'Feedback Status'))

    def __init__(self, *args, **kwargs):
        super(Research, self).__init__(*args, **kwargs)
        fields_iter = iter(self._meta.fields)
        for val, field in zip(args, fields_iter):
            if field.attname == 'end':
                if now() >= val:
                    if not self.is_complete:
                        self.is_complete = True
                        self.save()
                        if self.is_paid:
                            sr = ScientistResearch.objects.get(research__id=self.id)
                            userprofile = sr.scientist.userprofile
                            userprofile.available_balance += self.remain_credit
                            userprofile.save()
                            ScientistPaymentRecord(scientist=sr.scientist, credit=self.remain_credit,
                                                   description='refund from [id=%s, name=%s] research' % (
                                                       self.id, self.name)).save()
                break

    def __unicode__(self):
        return self.name

    def get_remind_time(self, time, type):
        seconds_count = 0
        if type == 'weeks':
            seconds_count = 604800 * time
        elif type == 'days':
            seconds_count = 86400 * time
        elif type == 'hours':
            seconds_count = 3600 * time
        elif type == 'minutes':
            seconds_count = 60 * time
            #return time.mktime((self.start - datetime.timedelta(seconds=seconds_count)).timetuple())
        return seconds_count

    def get_distance(self, request):
        user_type = request.session['user_type']
        basic_info = request.user.userprofile.basic_info.get(user_type, None)
        if basic_info:
            lat1 = basic_info.get('lat', None)
            lng1 = basic_info.get('lat', None)
            lat2 = self.location.lat if self.location else None
            lng2 = self.location.lng if self.location else None

            if lat1 and lng1 and lat2 and lng2:
                rad_lat1 = self.rad(lat1)
                rad_lat2 = self.rad(lat2)
                a = rad_lat1 - rad_lat2
                b = self.rad(lng1) - self.rad(lng2)
                s = 2 * math.asin(
                    math.sqrt(
                        math.pow(math.sin(a / 2), 2) + math.cos(rad_lat1) * math.cos(rad_lat2) * math.pow(
                            math.sin(b / 2),
                            2)))
                earth_radius = 6378.137
                s *= earth_radius
                return abs(s)
        return 'N/A'

    def rad(self, d):
        return float(d) * math.pi / 180.0

    @property
    def remain_credit(self):
        try:
            assigned_credit_count = 0
            participant_list = ParticipantResearch.objects.filter(research=self)
            for participant in participant_list:
                assigned_credit_count += participant.award_credit
            return self.total_credit - assigned_credit_count
        except Exception as e:
            pass

    def get_nearest_event(self):
        events = self.researchevent_set.filter(start__gt=now()).order_by('start')
        if events:
            return events[0]
        else:
            return None

    def can_cancel(self):
        if datetime.datetime.now() + datetime.timedelta(seconds=3600) >= self.start:
            return False
        else:
            return True

    @property
    def is_feedback(self):
        participant_ids = self.get_participant_ids()
        recipient_ids = self.get_recipient_ids()
        count = len(participant_ids)
        ids = [pid for pid in recipient_ids if pid in participant_ids]
        if len(ids) == count:
            return True
        else:
            return False

    def get_recipient_ids(self):
        recipient_ids = []
        messages = Message.objects.filter_message(content_object=self, type=TYPE_FEEDBACK)
        for message in messages:
            recipient_ids.append(message.recipient.id)
        return recipient_ids

    def get_participant_ids(self):
        participant_ids = []
        pr_list = ParticipantResearch.objects.filter(research=self, confirmed=True)
        for pr in pr_list:
            participant_ids.append(pr.participant.id)
        return participant_ids

    #def save(self, force_insert=False, force_update=False, using=None,
    #         update_fields=None):
    #    super(Research, self).save(force_insert, force_update)
    #    #research_saved.send(sender=Research, research=self)


class ResearchEvent(TimeStampedModel):
    research = models.ForeignKey(Research)
    start = models.DateTimeField(verbose_name=_(u'Start time'))
    end = models.DateTimeField(verbose_name=_(u'End time'))
    is_participant_sent = models.BooleanField(default=False)
    is_scientist_sent = models.BooleanField(default=False)

    def to_dict(self):
        title = self.research.name
        description = self.research.description
        total_participant_num = self.research.need_participant_num
        join_participant_num = ParticipantResearchEvent.objects.filter(research_event=self).count()
        scientist = ScientistResearch.objects.filter(research=self.research)[0].scientist

        data = {
            'id': self.id,
            'title': title,
            'description': description,
            'start': self.start.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'end': self.end.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'scientist_name': scientist.username,
            'total_participant_num': total_participant_num,
            'join_participant_num': join_participant_num
        }
        return data


class ResearchCategory(TimeStampedModel):
    '''
    The model store the researcher and category relationship
    '''
    category = models.ForeignKey(Category, verbose_name=_(u'Research Type'))
    research = models.ForeignKey(Research)


class Math(object):
    pass


class ParticipantResearch(TimeStampedModel):
    '''
    The model store the relationship between participants and the research.
    '''
    participant = models.ForeignKey(User, verbose_name=_(u'Participant'))
    research = models.ForeignKey(Research)
    confirmed = models.BooleanField(verbose_name=_(u'Confirmed'), default=False)
    award_credit = models.FloatField(default=0)
    donate_credit = models.FloatField(default=0)

    scientist_award_dt = models.DateTimeField(null=True, blank=True)
    participant_resp = models.NullBooleanField(null=True, blank=True)
    participant_resp_dt = models.DateTimeField(null=True, blank=True)
    superuser_award_dt = models.DateTimeField(null=True, blank=True)
    payment_type = models.CharField(null=True, blank=True, choices=PAYMENT_TYPE_CHOICES, max_length=10)
    payment_status = models.NullBooleanField(null=True, blank=True)
    payment_resp = models.CharField(null=True, blank=True, max_length=1024)
    payment_account = models.CharField(null=True, blank=True, max_length=255)


class ScientistResearch(TimeStampedModel):
    '''
    The model store the relationship between researcher (or scientist) and the research
    '''
    scientist = models.ForeignKey(User, verbose_name=_(u'Scientist'))
    research = models.ForeignKey(Research)


class ParticipantResearchEvent(TimeStampedModel):
    participant = models.ForeignKey(User, verbose_name=_(u'Participant'))
    research_event = models.ForeignKey(ResearchEvent, verbose_name=_(u'Research Event'))


class RemindParticipantInfo(TimeStampedModel):
    research = models.ForeignKey(Research, verbose_name=_(u'Reminder research'))
    time = models.PositiveIntegerField(verbose_name=_(u'Reminder before time'), default=0)
    message = models.CharField(verbose_name=_(u'Participants reminder message'), max_length=255, null=True, blank=True)
    type = models.CharField(verbose_name=_(u'Reminder type'), max_length=20, default='email')
    time_type = models.CharField(verbose_name=_(u'Time type'), max_length=20, default='minutes')

    def get_remind_participant_time(self):
        return self.research.get_remind_time(self.time, self.time_type)


class RemindScientistInfo(TimeStampedModel):
    research = models.ForeignKey(Research, verbose_name=_(u'Reminder research'))
    time = models.PositiveIntegerField(verbose_name=_(u'Reminder before time'), default=0)
    message = models.CharField(verbose_name=_(u'Scientist reminder message'), max_length=255, null=True, blank=True)
    type = models.CharField(verbose_name=_(u'Reminder type'), max_length=20, default='email')
    time_type = models.CharField(verbose_name=_(u'Time type'), max_length=20, default='minutes')

    def get_remind_scientist_time(self):
        return self.research.get_remind_time(self.time, self.time_type)


class ScientistPaymentRecord(TimeStampedModel):
    scientist = models.ForeignKey(User, verbose_name=_(u'Scientist'))
    credit = models.FloatField(verbose_name=_(u'Credit'), null=True, blank=True, default=0)
    description = models.TextField(verbose_name=_(u'Description'), max_length=1024, null=True, blank=True)


class DonateRecord(TimeStampedModel):
    user = models.ForeignKey(User, null=True, blank=True, verbose_name=_(u'Donate of user'))
    donate_amount = models.FloatField(default=0, verbose_name=_(u'The amount of the donation'))


class AnonymousDonateRecord(TimeStampedModel):
    first_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_(u'First Name'))
    last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_(u'Last Name'))
    email = models.EmailField(max_length=255, null=True, blank=True, verbose_name=_(u'Email Address'))
    donate_amount = models.FloatField(default=0, verbose_name=_(u'Amount of the donation'))


class DonateSetting(TimeStampedModel):
    key = models.CharField(max_length=255, null=True, blank=True, verbose_name=_(u'Key'))
    value = models.CharField(max_length=255, null=True, blank=True, verbose_name=_(u'Value'))


'''
research_saved = Signal(providing_args=['research'])


def generate_events(sender, research, **kwargs):
    """
    A signal receiver which generate events for research
    """
    if research.is_publish:
        research.researchevent_set.all().delete()
        for day in rrule(DAILY, dtstart=research.start, until=research.end, byweekday=(MO, TU, WE, TH, FR)):
            start = timezone.make_aware(day.replace(hour=9, tzinfo=None), timezone.get_current_timezone())
            end = timezone.make_aware(day.replace(hour=15, tzinfo=None), timezone.get_current_timezone())
            event = ResearchEvent(research=research, start=start, end=end)
            event.save()


research_saved.connect(generate_events, sender=Research)
'''


def update_research_paid_info(sender, **kwargs):
    ipn_obj = sender
    # Undertake some action depending upon `ipn_obj`.
    try:
        custom = ipn_obj.custom
        if custom == 'donate':
            first_name = ipn_obj.first_name
            last_name = ipn_obj.last_name
            payer_email = ipn_obj.payer_email
            donate_amount = ipn_obj.payment_gross
            AnonymousDonateRecord(first_name=first_name, last_name=last_name, email=payer_email,
                                  donate_amount=donate_amount).save()
        else:
            sr = ScientistResearch.objects.get(research__id=int(custom))
            research = sr.research
            research.is_paid = True
            research.is_publish = True
            research.payment_dt = now()
            research.save()

            ScientistPaymentRecord(scientist=sr.scientist, credit=research.total_credit,
                                   description='recharge to account').save()

            ScientistPaymentRecord(scientist=sr.scientist, credit=-research.total_credit,
                                   description='payment for [id=%s, name=%s] research' % (
                                   research.id, research.name)).save()
    except Research.DoesNotExist:
        pass

payment_was_successful.connect(update_research_paid_info)
