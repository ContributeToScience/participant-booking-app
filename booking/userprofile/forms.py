from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from allauth.account.forms import SignupForm, LoginForm
from allauth.account import app_settings

from userprofile.models import UserProfile
from core.utils import USER_TYPE_CHOICES
from core.utils import USER_TYPE


PAYMENT_TYPE_CHOICES = (
    ('paypal', _(u'PayPal')),
    ('amazon', _(u'Amazon')),
)


class CommonForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True, label=_(u'First name'))
    middle_name = forms.CharField(max_length=30, required=False, label=_(u'Middle name'))
    last_name = forms.CharField(max_length=30, required=True, label=_(u'Last name'))
    address = forms.CharField(max_length=255, required=True, label=_(u'Approximate address'))
    lng = forms.CharField(required=True, label=_(u'Longitude'), max_length=255)
    lat = forms.CharField(required=True, label=_(u'Latitude'), max_length=255)
    mobile = forms.CharField(max_length=30, required=False, label=_(u'Mobile number'))
    payment_type = forms.ChoiceField(required=False, label=_(u'Payment type'), choices=PAYMENT_TYPE_CHOICES)
    payment_account = forms.CharField(max_length=30, required=False, label=_(u'Payment id'))

    class Meta:
        model = UserProfile
        exclude = (
            'available_balance',
        )


class ParticipantSignupForm(SignupForm):
    def create_user(self, commit=True):
        user = super(ParticipantSignupForm, self).create_user()

        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        user_profile.is_participant = True
        user_profile.save()

        return user


class ScientistSignupForm(SignupForm):
    def create_user(self, commit=True):
        user = super(ScientistSignupForm, self).create_user()

        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        user_profile.is_scientist = True
        user_profile.is_participant = True
        user_profile.save()

        return user


class DepartmentSignupForm(SignupForm):
    def create_user(self, commit=True):
        user = super(DepartmentSignupForm, self).create_user()

        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        user_profile.is_department = True
        user_profile.is_scientist = True
        user_profile.is_participant = True
        user_profile.save()

        return user


class NewLoginForm(LoginForm):
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)

    def clean(self):
        if self._errors:
            return
        user = authenticate(**self.user_credentials())
        if user:
            if user.is_active:
                self.user = user
                user_type = self.data['user_type']
                if not user_type or user_type not in USER_TYPE:
                    raise forms.ValidationError(_("Incorrect user type."))
                profile = UserProfile.objects.get_or_create(user=user)[0]
                if not profile.has_role(user_type):
                    raise forms.ValidationError(_("The user do not have the user type: %s." % user_type))
            else:
                raise forms.ValidationError(_("This account is currently"
                                              " inactive."))
        else:
            if app_settings.AUTHENTICATION_METHOD == 'email':
                error = _("The e-mail address and/or password you specified"
                          " are not correct.")
            elif app_settings.AUTHENTICATION_METHOD == 'username':
                error = _("The username and/or password you specified are"
                          " not correct.")
            else:
                error = _("The login and/or password you specified are not"
                          " correct.")
            raise forms.ValidationError(error)
        return self.cleaned_data