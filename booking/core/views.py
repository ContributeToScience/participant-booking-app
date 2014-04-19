import json

from avatar.templatetags.avatar_tags import avatar_url
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseNotAllowed, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings

from avatar.models import Avatar

from core.utils import USER_TYPE_PARTICIPANT, USER_TYPE_SCIENTIST, USER_TYPE_DEPARTMENT
from userprofile.models import UserProfile


@login_required
def upload_avatar(request):
    '''
    Upload avatar
    :param request:
    :return:
    '''
    if request.method == 'POST':
        avatar_file = request.FILES['file']
        avatar = Avatar(
            user=request.user,
            primary=True,
        )
        try:
            avatar.avatar.delete()
        except Exception as e:
            # TODO log e
            pass
        avatar.avatar.save(avatar_file.name, avatar_file)
        avatar.save()
        avatar.create_thumbnail(80)
        return_data = json.dumps(
            {'status': 'success', 'thumbnail_url': avatar_url(request.user, 80)})
        return HttpResponse(return_data, mimetype='application/json')
    return HttpResponseNotAllowed(['POST', ])


def home(request, template='home.html', extra_context=None):
    """
    Home page

    **Context**

    ``RequestContext``

    **Template:**

    :template:`home.html`

    """
    if request.user.is_staff:
        return HttpResponseRedirect(reverse('award_participants'))
    elif request.user.is_authenticated():
        if request.session.get('user_type') == USER_TYPE_PARTICIPANT:
            return HttpResponseRedirect(reverse('participant'))
        elif request.session.get('user_type') == USER_TYPE_SCIENTIST:
            return HttpResponseRedirect(reverse('scientist'))
        elif request.session.get('user_type') == USER_TYPE_DEPARTMENT:
            return HttpResponseRedirect(reverse('department'))

    context = {
        'action': settings.PAYPAL_ACTION,
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'notify_url': '%s%s' % (settings.SITE_NAME, reverse_lazy('paypal-ipn')),
        'return_url': '%s%s' % (settings.SITE_NAME, reverse_lazy('anonymous_donate_paypal_complete')),
        'cancel_return': '%s%s' % (settings.SITE_NAME, reverse_lazy('home')),
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def signup_success(request, template='socialaccount/signup_success.html', extra_context=None):
    userprofile = UserProfile.objects.filter(user=request.user)

    if request.method == 'POST':
        user_type = request.POST.get('user_type', USER_TYPE_PARTICIPANT)
        userprofile[0].set_role(user_type)

    if userprofile and len(userprofile) > 0:
        roles = userprofile[0].get_roles()
        request.session['user_type'] = roles[-1]
        return HttpResponseRedirect(reverse_lazy('home'))
    else:
        UserProfile(user=request.user, is_participant=True).save()

    context = {

    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))