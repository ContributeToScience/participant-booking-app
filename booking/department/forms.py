from django import forms
from django.utils.translation import ugettext_lazy as _

from userprofile.forms import CommonForm


class DepartmentBasicInfoForm(CommonForm):
    credit_scheme_name = forms.CharField(required=False, label=_(u'Name of credit scheme'))
    department = forms.CharField(required=False, label=_(u'Department'))
    university = forms.CharField(required=False, label=_(u'University'))


class DepartmentSchemeForm(forms.Form):
    name = forms.CharField(label=_(u'Name'), max_length=100)
    start = forms.DateField(required=True,
                            label=_(u'Start date'),
                            widget=forms.DateInput(attrs={
                                'class': 'datepick',
                                'data-rule-required': 'true',
                                'data-rule-dateiso': 'true',
                                'data-date-format': 'yyyy-mm-dd'})
    )
    end = forms.DateField(required=True,
                          label=_(u'End date'),
                          widget=forms.DateInput(attrs={
                              'class': 'datepick',
                              'data-rule-required': 'true',
                              'data-rule-dateiso': 'true',
                              'data-date-format': 'yyyy-mm-dd'})
    )
    total_credit = forms.IntegerField(min_value=0, label=_(u'Total credits'))


class DepartmentSchemeLocationForm(forms.Form):
    department = forms.CharField(required=True, label=_(u'Department'), max_length=255)
    university = forms.CharField(required=True, label=_(u'University'), max_length=255)
    address = forms.CharField(required=False, label=_(u'Location (address, room)'), max_length=255)
    lng = forms.CharField(required=False, label=_(u'Longitude'), max_length=255)
    lat = forms.CharField(required=False, label=_(u'Latitude'), max_length=255)