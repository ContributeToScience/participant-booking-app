from model_utils.models import TimeStampedModel
from json_field import JSONField

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.utils import USER_TYPE_PARTICIPANT, USER_TYPE_SCIENTIST, USER_TYPE_DEPARTMENT, encrypt, decrypt


class UserProfile(TimeStampedModel):
    user = models.OneToOneField(User)
    is_participant = models.BooleanField(verbose_name=_(u'Is Participant ?'), default=False)
    is_scientist = models.BooleanField(verbose_name=_(u'Is Scientist ?'), default=False)
    is_department = models.BooleanField(verbose_name=_(u'Is Department ?'), default=False)
    basic_info = JSONField(verbose_name=_(u'Basic Info'), null=True, blank=True, default='{}')
    question = JSONField(verbose_name=_(u'Setting'), null=True, blank=True, default='{}')
    available_balance = models.FloatField(null=True, blank=True, default=0)

    def __init__(self, *args, **kwargs):
        super(UserProfile, self).__init__(*args, **kwargs)
        self._iter(self.basic_info, False)
        #fields_iter = iter(self._meta.fields)
        #for val, field in zip(args, fields_iter):
        #    if field.attname == 'basic_info':
        #        val = val.replace('null', 'None').replace('true', 'True').replace('false', 'False')
        #        basic_info = eval(val)
        #        self._iter(basic_info, False)
        #        self.basic_info = basic_info
        #        break

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self._iter(self.basic_info)
        super(UserProfile, self).save(force_insert, force_update)
        self._iter(self.basic_info, False)

    def _iter(self, dict, is_encrypt=True):
        for user_type in dict:
            for key in dict[user_type]:
                if key.find('_name') != -1 or key.find('address') != -1:
                    if is_encrypt:
                        dict[user_type][key] = encrypt(dict[user_type][key])
                    else:
                        dict[user_type][key] = decrypt(dict[user_type][key])

    def get_roles(self):
        roles = filter(lambda x: self.has_role(x), [USER_TYPE_PARTICIPANT, USER_TYPE_SCIENTIST, USER_TYPE_DEPARTMENT])
        return roles

    def has_role(self, user_type):
        if user_type == USER_TYPE_PARTICIPANT:
            return self.is_participant
        elif user_type == USER_TYPE_SCIENTIST:
            return self.is_scientist
        elif user_type == USER_TYPE_DEPARTMENT:
            return self.is_department
        else:
            return False

    def set_role(self, user_type, status=True):
        if user_type == USER_TYPE_PARTICIPANT:
            self.is_participant = status
        elif user_type == USER_TYPE_SCIENTIST:
            self.is_scientist = status
        elif user_type == USER_TYPE_DEPARTMENT:
            self.is_department = status
        else:
            pass
        self.save()

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = ''
        key = self.basic_info.keys()[0] if self.basic_info.keys() else ''
        basic_info = self.basic_info.get(key, None)
        if basic_info:
            first_name = basic_info.get('first_name', '')
            last_name = basic_info.get('last_name', '')
            full_name = ('%s %s' % (first_name, last_name)).strip()
        if not full_name:
            full_name = self.user.username
        return full_name
