from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from django.utils.translation import ugettext_lazy as _

from userprofile.forms import CommonForm

from core.utils import GENDER_CHOICES, UNIVERSITY_RESEARCH_CHOICES, BUSINESS_RESEARCH_CHOICES


class ParticipantBasicInfoForm(CommonForm):
    biological_info = forms.CharField(required=False, label=_(u'Biological info'))
    dob = forms.DateField(required=False, label=_(u'Date of birthday'), widget=forms.DateInput(
        attrs={'class': 'datepick', 'data-rule-required': 'true', 'data-rule-dateiso': 'true',
               'data-date-format': 'yyyy-mm-dd'}))
    gender = forms.ChoiceField(required=False, label=_(u'Gender'), choices=GENDER_CHOICES)
    email_me = forms.BooleanField(required=False, label=_(u'email me when there is a new study in my area'))
    some_research = forms.BooleanField(required=False, label=_(
        u'some research is concerned with comparing results of people from, for example, different places in the world. I am happy to be emailed about such person-specific research'))


class ParticipantQuestionForm(forms.Form):
    university_research = forms.MultipleChoiceField(required=False,
                                                    label=_(u'what university research you want to hear about?'),
                                                    widget=CheckboxSelectMultiple,
                                                    choices=UNIVERSITY_RESEARCH_CHOICES)

    business_research = forms.MultipleChoiceField(required=False,
                                                  label=_(u'what business research you want to hear about?'),
                                                  widget=CheckboxSelectMultiple,
                                                  choices=BUSINESS_RESEARCH_CHOICES)

    is_help = forms.BooleanField(required=False, label=_(
        u'not all academic studies have funding. Would you be willing to help further science by taking part in studies where there is little or no funding?'))

    is_online = forms.BooleanField(required=False, label=_(u'willing to do research on your home computer, online?'))

    research_time = forms.CharField(required=False, label=_(u'when are you typically available to do research?'))

    is_agreement = forms.BooleanField(required=False, label=_(
        u'want to be a science altruist\'bla bla bla, very special, do science for free if I so wish, donating money to research fun\''))