import json
from allauth.account.forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages import error
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import login as django_login

from allauth.account.utils import get_next_redirect_url
from allauth.account.views import SignupView, LoginView

from .models import UserProfile
from .forms import ParticipantSignupForm, DepartmentSignupForm, ScientistSignupForm, NewLoginForm
from department.forms import DepartmentBasicInfoForm
from participant.forms import ParticipantBasicInfoForm, ParticipantQuestionForm
from scientist.forms import ScientistBasicInfoForm
from core.utils import USER_TYPE_PARTICIPANT, USER_TYPE_SCIENTIST, USER_TYPE_DEPARTMENT, USER_TYPE, get_location, errors_to_json, json_result


class NewLoginView(LoginView):
    form_class = NewLoginForm

    def get_success_url(self):
        user_type = self.request.REQUEST.get('user_type')
        self.request.session['user_type'] = user_type
        self.success_url = reverse_lazy(user_type)
        ret = (get_next_redirect_url(self.request,
                                     self.redirect_field_name)
               or self.success_url)
        return ret


class ParticipantSignupView(SignupView):
    template_name = 'userprofile/signup.html'
    form_class = ParticipantSignupForm
    redirect_field_name = 'next'
    success_url = None

    def get_success_url(self):
        self.request.session['user_type'] = USER_TYPE_PARTICIPANT
        return self.kwargs['success_url']

    def get_context_data(self, **kwargs):
        ret = super(ParticipantSignupView, self).get_context_data(**kwargs)
        ret.update(self.kwargs)
        return ret


class DepartmentSignupView(SignupView):
    template_name = 'userprofile/signup.html'
    form_class = DepartmentSignupForm
    redirect_field_name = 'next'
    success_url = None

    def get_success_url(self):
        self.request.session['user_type'] = USER_TYPE_DEPARTMENT
        return self.kwargs['success_url']

    def get_context_data(self, **kwargs):
        ret = super(DepartmentSignupView, self).get_context_data(**kwargs)
        ret.update(self.kwargs)
        return ret


class ScientistSignupView(SignupView):
    template_name = 'userprofile/signup.html'
    form_class = ScientistSignupForm
    redirect_field_name = 'next'
    success_url = None

    def get_success_url(self):
        self.request.session['user_type'] = USER_TYPE_SCIENTIST
        return self.kwargs['success_url']

    def get_context_data(self, **kwargs):
        ret = super(ScientistSignupView, self).get_context_data(**kwargs)
        ret.update(self.kwargs)
        return ret


login = NewLoginView.as_view()
participant_signup = ParticipantSignupView.as_view()
department_signup = DepartmentSignupView.as_view()
scientist_signup = ScientistSignupView.as_view()


@login_required
def userprofile_basic_info(request, form_class, success_url, user_type, template, extra_context=None):
    """
    User basic_info

    **Context**

    ``RequestContext``

    """
    if not user_type or user_type not in USER_TYPE:
        raise Http404

    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            if len(user_profile.get_roles()) <= 0:
                user_profile.set_role(user_type)
            user_profile.basic_info[user_type] = form.cleaned_data
            first_name = form.cleaned_data.get('first_name', None)
            middle_name = form.cleaned_data.get('middle_name', None)
            last_name = form.cleaned_data.get('last_name', None)

            for key in USER_TYPE:
                basic_info = user_profile.basic_info.get(key, None)
                if basic_info:
                    basic_info['first_name'] = first_name
                    basic_info['middle_name'] = middle_name
                    basic_info['last_name'] = last_name
                else:
                    user_profile.basic_info[key] = {
                        'first_name': first_name,
                        'middle_name': middle_name,
                        'last_name': last_name,
                    }

            user_profile.save()

            '''
            user = user_profile.user
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            '''
            return HttpResponseRedirect(success_url)
    else:
        location = get_location(request)

        initial = {
            'address': '',
            'lng': location['lng'],
            'lat': location['lat'],
        }
        basic_info = user_profile.basic_info.get(user_type, None)
        if basic_info:
            initial.update(basic_info)
        form = form_class(initial=initial)

    context = {
        'form': form,
        'user_type': user_type,
    }
    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def userprofile_questions(request, form_class, success_url, user_type, template, extra_context=None):
    """
    User questions

    **Context**

    ``RequestContext``

    """
    if not user_type or user_type not in USER_TYPE:
        raise Http404

    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]

    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            if len(user_profile.get_roles()) <= 0:
                user_profile.set_role(user_type)
            user_profile.question[user_type] = form.cleaned_data
            user_profile.save()

            return HttpResponseRedirect(success_url)
    else:
        form = form_class(initial=user_profile.question.get(user_type, None))

    context = {
        'form': form,
        'user_type': user_type,
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def userprofile(request, username, template='userprofile/userprofile.html', extra_context=None):
    """
    User profile

    **Context**

    ``RequestContext``

    **Template:**

    :template:`userprofile/userprofile.html`

    """
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(UserProfile, user=user)
    context = {
        'user_profile': user_profile,
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def basic_info(request, username, extra_context=None):
    user_type = request.session.get('user_type')
    return redirect_profile(request, user_type)


def redirect_profile(request, user_type):
    if user_type == USER_TYPE_DEPARTMENT:
        return userprofile_basic_info(request, DepartmentBasicInfoForm, reverse_lazy(user_type), user_type,
                                      'userprofile/department_basic_info.html')
    elif user_type == USER_TYPE_PARTICIPANT:
        return userprofile_basic_info(request, ParticipantBasicInfoForm, reverse_lazy(user_type), user_type,
                                      'userprofile/participant_basic_info.html')
    elif user_type == USER_TYPE_SCIENTIST:
        return userprofile_basic_info(request, ScientistBasicInfoForm, reverse_lazy(user_type), user_type,
                                      'userprofile/scientist_basic_info.html')
    else:
        return HttpResponseRedirect(reverse_lazy('home'))


@login_required
def userrole(request, template='userprofile/userrole.html', extra_context=None):
    context = {

    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def switch_userrole(request, user_type):
    profile = request.user.userprofile

    if profile.has_role(user_type):
        request.session['user_type'] = user_type
        return HttpResponseRedirect(reverse_lazy(user_type))
    elif request.session['user_type'] == USER_TYPE_PARTICIPANT and user_type == USER_TYPE_DEPARTMENT:
        error(request, _(u'You must have a scientist role then switch department role'))
        return HttpResponseRedirect(reverse_lazy('userrole'))
    else:
        request.session['user_type'] = user_type
        profile.set_role(user_type)
        return HttpResponseRedirect(reverse_lazy('basic_info', args=[request.user.username, ]))


@login_required
def question_info(request, username, extra_context=None):
    user_type = request.session.get('user_type')
    return redirect_question(request, user_type)


def redirect_question(request, user_type):
    if user_type == USER_TYPE_PARTICIPANT:
        return userprofile_questions(request, ParticipantQuestionForm, reverse_lazy(user_type), user_type,
                                     'userprofile/participant_question_info.html')


@login_required
def account(request, template='userprofile/delete_account.html', extra_context=None):
    context = {
        'roles': request.user.userprofile.get_roles(),
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def delete_account(request, user_type):
    if user_type != USER_TYPE_PARTICIPANT:
        profile = request.user.userprofile
        for role in profile.get_roles():
            if __get_role_level(role) > __get_role_level(user_type):
                error(request, _(u'You must first remove the top level of role'))
                return HttpResponseRedirect(reverse_lazy('account'))
        profile.set_role(user_type, False)
        if user_type == USER_TYPE_DEPARTMENT:
            request.session['user_type'] = USER_TYPE_SCIENTIST
        else:
            request.session['user_type'] = USER_TYPE_PARTICIPANT
        return HttpResponseRedirect(reverse_lazy('basic_info', args=[request.user.username, ]))
    else:
        error(request, _(u'You can not delete participant role'))
        return HttpResponseRedirect(reverse_lazy('account'))


def __get_role_level(user_type):
    if user_type == USER_TYPE_PARTICIPANT:
        return 1
    elif user_type == USER_TYPE_SCIENTIST:
        return 2
    elif user_type == USER_TYPE_DEPARTMENT:
        return 3
    else:
        return 0


def ajax_login_signup(request):
    if request.is_ajax() and request.method == 'POST':
        type = request.POST.get('type', 'login')
        if type == 'login':
            return ajax_login(request)
        else:
            return ajax_signup(request)
    else:
        return render_to_response("account/ajax_login_signup.html", {}, context_instance=RequestContext(request))


def ajax_login(request):
    if request.is_ajax() and request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, request.user)
            data = {'status': 'success'}
        else:
            data = json.loads(errors_to_json(form.errors))
        return json_result(request, data)
    else:
        return render_to_response("account/ajax_login.html", {}, context_instance=RequestContext(request))


def ajax_signup(request):
    if request.is_ajax() and request.method == 'POST':
        user_type = request.POST.get('user_type', USER_TYPE_PARTICIPANT)
        if user_type == USER_TYPE_SCIENTIST:
            form = ScientistSignupForm(request.POST)
        elif user_type == USER_TYPE_DEPARTMENT:
            form = DepartmentSignupForm(request.POST)
        else:
            form = ParticipantSignupForm(request.POST)
        if form.is_valid():
            user = form.save(request)
            request.session['user_type'] = user_type
            if not hasattr(user, 'backend'):
                user.backend = "django.contrib.auth.backends.ModelBackend"
            django_login(request, user)
            data = {'status': 'success'}
        else:
            data = json.loads(errors_to_json(form.errors))
        return json_result(request, data)
    else:
        user_type = request.REQUEST.get('user_type', USER_TYPE_PARTICIPANT)
        next = request.REQUEST.get('next', None)
        context = {
            'user_type': user_type if user_type else USER_TYPE_PARTICIPANT,
            'next': next,
        }
        return render_to_response("account/ajax_signup.html", context, context_instance=RequestContext(request))