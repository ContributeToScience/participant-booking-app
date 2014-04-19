from uuid import uuid4

from django.utils.translation import ugettext as _


STATUS_PENDING = 0
STATUS_ACCEPTED = 1
STATUS_REJECTED = 2

STATUS_CHOICES = (
    (STATUS_PENDING, _(u'Pending')),
    (STATUS_ACCEPTED, _(u'Accepted')),
    (STATUS_REJECTED, _(u'Rejected')),
)

TYPE_DEFAULT = 0
TYPE_CANCEL_RESEARCH = 1
TYPE_FEEDBACK = 2
TYPE_REPORT_BUG = 3

TYPE_CHOICES = (
    (TYPE_DEFAULT, _(u'Default')),
    (TYPE_CANCEL_RESEARCH, _(u'Cancel Research')),
    (TYPE_FEEDBACK, _(u'Feedback')),
    (TYPE_REPORT_BUG, _(u'Report Bug')),
)


def get_uuid4_id():
    return str(uuid4())