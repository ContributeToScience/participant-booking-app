import datetime
from django import template
from django.template.loader import get_template
from django.template import Context

from bootstrap_toolkit.templatetags.bootstrap_toolkit import get_pagination_context

from message.models import Message
from scientist.models import Research

register = template.Library()


@register.filter
def get_new_message_count(request):
    return Message.objects.filter(recipient=request.user, read_at__isnull=True).count()


@register.filter
def message_pagination(page, pages_to_show=10):
    context = get_pagination_context(page.object_list, pages_to_show)
    context.update({
        'total_number': page._get_count()
    })
    return get_template("message/_tpl/pagination.html").render(Context(context))


@register.inclusion_tag('message/_tpl/send_message.html')
def send_message(recipient_id, content_object_id):
    return {'recipient_id': recipient_id, 'content_object_id': content_object_id}


@register.inclusion_tag('message/_tpl/request_cancel.html')
def request_cancel(recipient_id, content_object_id):
    content = {
        'recipient_id': recipient_id,
        'content_object_id': content_object_id,
        'is_show': False,
    }
    research = Research.objects.get(id=content_object_id)
    if research.can_cancel():
        content.update({'is_show': True})
    return content


@register.inclusion_tag('message/_tpl/feedback.html')
def feedback(recipient_id, content_object_id):
    content = {
        'recipient_id': recipient_id,
        'content_object_id': content_object_id,
    }
    research = Research.objects.get(id=content_object_id)
    messages = Message.objects.filter_message(content_object=research, recipient__id=recipient_id)
    if messages and len(messages) > 0:
        content.update({'message_id': messages[0].id})
    return content


@register.inclusion_tag('message/_tpl/report_bug.html')
def report_bug(recipient_id, content_object_id):
    return {'recipient_id': recipient_id, 'content_object_id': content_object_id}