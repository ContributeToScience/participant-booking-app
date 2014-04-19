import datetime
import json
from core.utils import is_integer
from django import forms
from django.utils.translation import ugettext_lazy as _

from userprofile.forms import CommonForm

from .models import Research


class ScientistBasicInfoForm(CommonForm):
    academic_position = forms.CharField(required=False, label=_(u'Academic position'))
    department = forms.CharField(required=False, label=_(u'Department'))
    university = forms.CharField(required=False, label=_(u'University'))
    country = forms.CharField(required=False, label=_(u'Country'))


class ResearchForm(forms.ModelForm):
    name = forms.CharField(required=True, label=_(u'Research name'),
                           widget=forms.TextInput(attrs={'data-rule-required': 'true', 'data-rule-maxlength': 100, }))

    need_participant_num = forms.IntegerField(required=True, label=_(u'Number of participants needed'),
                                              widget=forms.TextInput(
                                                  attrs={'class': 'spinner', 'data-rule-required': 'true',
                                                         'data-rule-number': 'true', }))

    description = forms.CharField(required=False, label=_(u'Description'),
                                  widget=forms.Textarea(attrs={'data-rule-maxlength': 1024}))

    address = forms.CharField(required=False, label=_(u'Location'),
                              widget=forms.TextInput(attrs={'data-rule-maxlength': 255}))

    lng = forms.CharField(required=False, label=_(u'Longitude'),
                          widget=forms.TextInput(attrs={'data-rule-maxlength': 255}))

    lat = forms.CharField(required=False, label=_(u'Latitude'),
                          widget=forms.TextInput(attrs={'data-rule-maxlength': 255}))

    room = forms.CharField(required=False, label=_(u'Room'), widget=forms.TextInput(attrs={'data-rule-maxlength': 255}))

    url = forms.URLField(required=False, label=_(u'Web url'),
                         widget=forms.TextInput(attrs={'data-rule-url': 'true', 'data-rule-maxlength': 255}))

    start = forms.DateField(required=True, label=_(u'Start date'), widget=forms.DateInput(
        attrs={'class': 'datepick', 'data-rule-required': 'true', 'data-rule-dateiso': 'true',
               'data-date-format': 'yyyy-mm-dd'}))

    end = forms.DateField(required=True, label=_(u'End date'), widget=forms.DateInput(
        attrs={'class': 'datepick', 'data-rule-required': 'true', 'data-rule-dateiso': 'true',
               'data-date-format': 'yyyy-mm-dd'}))

    remind_scientist_info = forms.CharField(required=False, label=_(u'Remind scientist info'),
                                            widget=forms.TextInput(attrs={'data-rule-maxlength': 1024}))

    remind_participant_info = forms.CharField(required=False, label=_(u'Remind participant info'),
                                              widget=forms.TextInput(attrs={'data-rule-maxlength': 1024}))

    default_event_duration = forms.IntegerField(required=True, min_value=10, max_value=360, label=_(u'Time/Experiment'),
                                                widget=forms.TextInput(
                                                    attrs={'class': 'spinner', 'data-rule-required': 'true',
                                                           'data-rule-number': 'true', }))

    class Meta:
        model = Research
        exclude = (
            'researcher',
            'created',
            'modified',
            'is_publish',
            'currency',
            'remuneration',
            'is_credit_scheme',
            'is_paid',
            'payment_dt',
            'is_complete',
            'feedback_status',
        )

    def clean(self):
        super(ResearchForm, self).clean()
        if 'start' in self.cleaned_data and 'end' in self.cleaned_data:
            if self.cleaned_data['start'] >= self.cleaned_data['end']:
                raise forms.ValidationError(_(u'The research start time should be less than end time.'))
            elif datetime.datetime.now() >= datetime.datetime.combine(self.cleaned_data['end'], datetime.time()):
                raise forms.ValidationError(_(u'The research end time should be more than current time.'))

        remind_scientist_info = json.loads(self.cleaned_data['remind_scientist_info'])
        remind_participant_info = json.loads(self.cleaned_data['remind_participant_info'])

        if remind_scientist_info and len(remind_scientist_info) > 0:
            for remind_scientist in remind_scientist_info:
                if is_integer(remind_scientist.get('time', 0)) <= 0:
                    raise forms.ValidationError(_(u'The scientist remind time can not be empty.'))

        if remind_participant_info and len(remind_participant_info) > 0:
            for remind_participant in remind_participant_info:
                if is_integer(remind_participant.get('time', 0)) <= 0:
                    raise forms.ValidationError(_(u'The participant remind time can not be empty.'))

        if 'is_feedback_promise' in self.cleaned_data and 'feedback_promise_time' in self.cleaned_data:
            if self.cleaned_data['is_feedback_promise'] and not self.cleaned_data['feedback_promise_time']:
                raise forms.ValidationError(_(u'Feedback promise time can not be empty.'))

        return self.cleaned_data