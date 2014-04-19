from model_utils.models import TimeStampedModel

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from scientist.models import Research


class StarRating(TimeStampedModel):
    from_user = models.ForeignKey(User, related_name='from_user_rating_set')
    to_user = models.ForeignKey(User, related_name='to_user_rating_set')
    research = models.ForeignKey(Research)
    user_type = models.CharField(verbose_name=_(u'User Type'), max_length=20, help_text=_(u'To user of user type, options: participant or scientist'))
    time_score = models.PositiveIntegerField(verbose_name=_(u'Time Score'), default=0, help_text=_(u'Time score, the highest 3 points'))
    attitude_score = models.PositiveIntegerField(verbose_name=_(u'Attitude Score'), default=0, help_text=_(u'Attitude_score, the highest 3 points'))