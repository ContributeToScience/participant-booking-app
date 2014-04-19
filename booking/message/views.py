from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages import success, error, warning
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from message.forms import MessageForm
from message.models import Message
from message.utils import TYPE_CANCEL_RESEARCH, TYPE_FEEDBACK
from scientist.models import Research, ParticipantResearch, ScientistResearch
from core.utils import get_page, json_result


@login_required
def message_post(request, template='message/message_post.html', extra_context=None):
    is_send = False
    research = None
    message = None
    content_object_id = request.GET.get('content_object_id', None)
    recipient_id = request.GET.get('recipient_id', None)
    type = request.GET.get('type', None)
    message_id = request.REQUEST.get('message_id', None)

    if message_id and message_id != 'None':
        message = Message.objects.get(id=message_id)

    if request.method == 'POST':
        form = MessageForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            content_object_id = form.cleaned_data.get('content_object_id', None)
            recipient_id = form.cleaned_data.get('recipient_id', None)
            subject = form.cleaned_data.get('subject', None)
            content = form.cleaned_data.get('content', None)
            type = form.cleaned_data.get('type', None)
            send_email = form.cleaned_data.get('send_email', False)

            if message:
                message.subject = subject
                message.content = content
                message.send_email = send_email
                message.save()
                is_send = True
            else:
                recipient_id = recipient_id.split(',') if recipient_id else []
                recipient_list = User.objects.filter(id__in=recipient_id if recipient_id else [])
                if recipient_list and len(recipient_list) > 0:
                    if content_object_id:
                        research = Research.objects.get(id=content_object_id)

                    for recipient in recipient_list:
                        if type == TYPE_CANCEL_RESEARCH and not research.can_cancel():
                            continue
                        if type == TYPE_FEEDBACK:
                            messages = Message.objects.filter_message(content_object=research, recipient=recipient)
                            if messages and len(messages) > 0:
                                continue
                        Message.objects.create_message(content_object=research, subject=subject, content=content, type=type,
                                                       sender=request.user, recipient=recipient, send_email=send_email)
                    success(request, _(u'Message was successfully sent.'))
                    is_send = True
    else:
        if message:
            form = MessageForm(initial={
                'subject': message.subject,
                'content': message.content,
                'send_email': message.send_email,
                'content_object_id': message.content_object.id,
                'recipient_id': message.recipient.id,
                'type': message.type,
                'message_id': message.id,
            })
        else:
            form = MessageForm(initial={
                'content_object_id': content_object_id,
                'recipient_id': recipient_id,
                'type': int(type) if type else type,
                'message_id': message_id,
            })

    context = {
        'form': form,
        'is_send': is_send
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def message_list(request, message_flag, template='message/message_list.html', extra_context=None):
    receive_messages = []
    send_messages = []
    trash_messages = []

    if message_flag == 'outbox':
        send_messages = Message.objects.filter(sender=request.user, sender_deleted_at__isnull=True)
    elif message_flag == 'trash':
        trash_messages = Message.objects.filter(
            Q(recipient=request.user, recipient_deleted_at__isnull=False) | Q(sender=request.user,
                                                                              sender_deleted_at__isnull=False))
    else:
        receive_messages = Message.objects.filter(recipient=request.user, recipient_deleted_at__isnull=True)

    receive_paginator = get_page(request, receive_messages, 10)
    send_paginator = get_page(request, send_messages, 10)
    trash_paginator = get_page(request, trash_messages, 10)

    context = {
        'receive_paginator': receive_paginator,
        'send_paginator': send_paginator,
        'trash_paginator': trash_paginator,
        'message_flag': message_flag,
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def message_delete(request):
    try:
        message_ids = request.POST.getlist('message_ids[]', [])
        messages = Message.objects.filter(id__in=message_ids)
        for message in messages:
            if message.sender == request.user:
                message.sender_deleted_at = now()
            if message.recipient == request.user:
                message.recipient_deleted_at = now()
            message.save()
        result = {'status': 'success'}
    except Exception as e:
        result = {'status': 'fail', 'reason': e.message}
    return json_result(request, result)


@login_required
def message_undo(request):
    try:
        message_ids = request.POST.getlist('message_ids[]', [])
        messages = Message.objects.filter(id__in=message_ids)
        for message in messages:
            if message.sender == request.user:
                message.sender_deleted_at = None
            if message.recipient == request.user:
                message.recipient_deleted_at = None
            message.save()
        result = {'status': 'success'}
    except Exception as e:
        result = {'status': 'fail', 'reason': e.message}
    return json_result(request, result)


@login_required
def message_detail(request, message_id, template='message/message_detail.html', extra_context=None):
    is_send = False
    message = get_object_or_404(Message, id=message_id)

    if message.sender != request.user and message.recipient != request.user:
        warning(request, _(u'You do not have permission to view this message'))
        return HttpResponseRedirect(reverse_lazy('message_list'))

    message.set_read(request.user)

    if request.method == 'POST':
        is_send = True
        status = request.POST.get('status', None)
        if status and message.is_pending_status():
            message.status = status
            message.save()
            if message.is_accepted_status():
                if message.is_cancel_research_type():
                    sr = ScientistResearch.objects.get(research=message.content_object)
                    if message.sender == sr.scientist:
                        pr = ParticipantResearch.objects.get(participant=message.recipient, research=sr.research,
                                                             confirmed=True)
                    else:
                        pr = ParticipantResearch.objects.get(participant=message.sender, research=sr.research,
                                                             confirmed=True)
                    pr.delete()
            elif message.is_rejected_status():
                pass
        else:
            warning(request, _(u'This message has been [%s]' % message.get_status_display()))

    context = {
        'is_send': is_send,
        'message': message,
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))