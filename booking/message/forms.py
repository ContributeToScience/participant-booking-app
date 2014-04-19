from django import forms
from django.utils.translation import ugettext_lazy as _


class MessageForm(forms.Form):
    message_id = forms.CharField(required=False)
    subject = forms.CharField(label=_(u'Subject'), max_length=120, required=False)
    content = forms.CharField(widget=forms.Textarea(), label=_(u'Message'), required=False)
    type = forms.IntegerField(required=True)
    send_email = forms.BooleanField(required=False)
    content_object_id = forms.CharField(required=False)
    recipient_id = forms.CharField(required=True)
