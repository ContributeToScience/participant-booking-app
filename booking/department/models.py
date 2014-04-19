from django.db import models
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User


class UniversityDepartment(TimeStampedModel):
    user = models.ForeignKey(User)
    university = models.CharField(verbose_name=_(u'University'), max_length=255)
    department = models.CharField(verbose_name=_(u'Department'), max_length=255)
    address = models.CharField(verbose_name=_(u'Address'), max_length=255, null=False, blank=False, default='')
    lng = models.FloatField(verbose_name=_(u'Longitude'), null=False, blank=False, default=0)
    lat = models.FloatField(verbose_name=_(u'Latitude'), null=False, blank=False, default=0)

    def __unicode__(self):
        return '%s %s' % (self.university, self.department)


class CreditScheme(TimeStampedModel):
    department = models.ForeignKey(User, verbose_name=_('Department'))
    name = models.CharField(verbose_name=_(u'Credit scheme name'), max_length=100)
    start = models.DateField(verbose_name=_(u'Start time'))
    end = models.DateField(verbose_name=_(u'End time'))
    university_department = models.ForeignKey(UniversityDepartment, null=True, blank=True)
    total_credit = models.PositiveIntegerField(verbose_name=_(u'Total Credits'), default=0)
    remain_credit = models.PositiveIntegerField(verbose_name=_(u'Remain Credits'), default=0)


class CoordinatorCreditScheme(TimeStampedModel):
    coordinator = models.ForeignKey(User, verbose_name=_(u'coordinator'))
    credit_scheme = models.ForeignKey(CreditScheme)


class ParticipantCreditScheme(TimeStampedModel):
    participant = models.ForeignKey(User, verbose_name=_(u'Participant'))
    credit_scheme = models.ForeignKey(CreditScheme)
    required_credit = models.PositiveIntegerField(verbose_name=_(u'Required Credits'), default=0)
    incomplete_credit = models.PositiveIntegerField(verbose_name=_(u'Incomplete Credits'), default=0)


class ScientistCreditScheme(TimeStampedModel):
    scientist = models.ForeignKey(User, verbose_name=_(u'Scientist'))
    credit_scheme = models.ForeignKey(CreditScheme)
    assigned_credit = models.PositiveIntegerField(verbose_name=_(u'Credits assigned'), default=0)
    remain_credit = models.PositiveIntegerField(verbose_name=_(u'Remain Credits'), default=0)


class SchemeCreditRecord(TimeStampedModel):
    credit_scheme = models.ForeignKey(CreditScheme)
    scientist = models.ForeignKey(User, verbose_name=_(u'Scientist'), related_name='scientist_creditrecord_set')
    participant = models.ForeignKey(User, verbose_name=_(u'Participant'), related_name='participant_creditrecord_set')
    allocated_credit = models.PositiveIntegerField(verbose_name=_(u'Allocated Credits'), default=0)