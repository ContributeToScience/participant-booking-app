from django.db.models.signals import post_save, pre_save
from model_utils.models import TimeStampedModel

from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _
from django.dispatch import Signal, receiver

from core.tasks import send_email
from message.managers import MessageManager
from message.utils import TYPE_CHOICES, STATUS_CHOICES, STATUS_PENDING, STATUS_ACCEPTED, TYPE_DEFAULT, STATUS_REJECTED, TYPE_CANCEL_RESEARCH, TYPE_FEEDBACK, TYPE_REPORT_BUG


class Message(TimeStampedModel):
    # Content-object field
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.IntegerField(null=True, blank=True)
    content_object = generic.GenericForeignKey(ct_field='content_type', fk_field='object_id')

    # Metadata about the message
    group_id = models.CharField(max_length=255, null=True, blank=True, verbose_name=_(u'Group Id'))
    type = models.IntegerField(choices=TYPE_CHOICES, default=TYPE_DEFAULT, verbose_name=_(u'Type'))
    subject = models.CharField(max_length=255, null=True, blank=True, verbose_name=_(u'Subject'))
    content = models.TextField(null=True, blank=True, verbose_name=_(u'Content'))
    sender = models.ForeignKey(User, related_name='sent_messages', null=True, blank=True, verbose_name=_(u'sender'))
    recipient = models.ForeignKey(User, related_name='received_messages', null=True, blank=True, verbose_name=_(u'recipient'))
    sent_at = models.DateTimeField(verbose_name=_(u'sent at'), default=now)
    read_at = models.DateTimeField(verbose_name=_(u'read at'), null=True, blank=True)
    sender_deleted_at = models.DateTimeField(verbose_name=_(u'deleted by sender at'), null=True, blank=True)
    recipient_deleted_at = models.DateTimeField(verbose_name=_(u'deleted by recipient at'), null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_PENDING, verbose_name=_(u'Status'))
    send_email = models.BooleanField(default=False, verbose_name=_(u'Send Email'))

    # Manager
    objects = MessageManager()

    class Meta:
        verbose_name = _("message")
        verbose_name_plural = _("messages")
        ordering = ['-sent_at', '-id']

    @property
    def is_new(self):
        """Tell if the recipient has not yet read the message."""
        return self.read_at is None

    def set_read(self, user):
        """
        Set message as read and accepted.
        """
        if self.read_at is None and self.recipient == user:
            self.read_at = now()
            if not self.is_cancel_research_type():
                self.status = STATUS_ACCEPTED
            self.save()

    def is_pending_status(self):
        """
        Tell if the message is in the pending state.
        """
        return self.status == STATUS_PENDING or self.status == str(STATUS_PENDING)

    def is_accepted_status(self):
        """
        Tell if the message is in the accepted state.
        """
        return self.status == STATUS_ACCEPTED or self.status == str(STATUS_ACCEPTED)

    def is_rejected_status(self):
        """
        Tell if the message is in the rejected state.
        """
        return self.status == STATUS_REJECTED or self.status == str(STATUS_REJECTED)

    def is_default_type(self):
        """
        Tell if the message is in the default type.
        """
        return self.type == TYPE_DEFAULT or self.type == str(TYPE_DEFAULT)

    def is_cancel_research_type(self):
        """
        Tell if the message is in the cancel research type.
        """
        return self.type == TYPE_CANCEL_RESEARCH or self.type == str(TYPE_CANCEL_RESEARCH)

    def is_feedback_type(self):
        """
        Tell if the message is in the feedback type.
        """
        return self.type == TYPE_FEEDBACK or self.type == str(TYPE_FEEDBACK)

    def is_report_bug_type(self):
        """
        Tell if the message is in the report bug type.
        """
        return self.type == TYPE_REPORT_BUG or self.type == str(TYPE_REPORT_BUG)


@receiver(post_save, sender=Message)
def post_message_handle(sender, instance, created, **kwargs):
    """
    Define a signal, when the message is successfully saved after the judge whether to send email
    @param sender: Message object
    @param instance: Message instance
    @param created: True is save otherwise is update
    @param kwargs:
    @return:
    """
    if created and instance.send_email:
        notification = {
            'subject': instance.subject,
            'recipient_list': [instance.recipient.email],
            'html_content': instance.content
        }
        send_email.delay(notification)

