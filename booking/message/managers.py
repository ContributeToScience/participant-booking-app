from django.db import models
from django.contrib.contenttypes.models import ContentType
from message.utils import get_uuid4_id


class MessageManager(models.Manager):

    def create_message(self, content_object, **kwargs):
        if content_object:
            content_type = ContentType.objects.get_for_model(content_object)
            if content_type.app_label == 'scientist' and content_type.name in ['research']:
                if not kwargs.get('group_id', None):
                    kwargs['group_id'] = get_uuid4_id()
                return self.get_or_create(content_type=content_type, object_id=content_object.id, **kwargs)
            else:
                raise Exception('Content type is invalid')
        else:
            if not kwargs.get('group_id', None):
                kwargs['group_id'] = get_uuid4_id()
            return self.get_or_create(**kwargs)

    def filter_message(self, content_object, **kwargs):
        content_type = ContentType.objects.get_for_model(content_object)
        if content_type.app_label == 'scientist' and content_type.name in ['research']:
            return self.filter(content_type=content_type, object_id=content_object.id, **kwargs)
        else:
            raise Exception('Content type is invalid')