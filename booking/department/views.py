import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages import success
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from avatar.templatetags.avatar_tags import avatar_url

from core.decorators import department_required
from core.utils import json_result, USER_TYPE_SCIENTIST, USER_TYPE_PARTICIPANT, get_location
from userprofile.models import UserProfile
from .forms import DepartmentSchemeForm, DepartmentSchemeLocationForm
from .models import CreditScheme, UniversityDepartment, ParticipantCreditScheme, ScientistCreditScheme, CoordinatorCreditScheme


@login_required
@department_required
def department(request, template='department/department.html', extra_context=None):
    scheme_list = CreditScheme.objects.filter(department=request.user)

    context = {
        'is_scheme': True if scheme_list else False,
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@department_required
def department_invite_participant(request, template='department/department_invite_participant.html',
                                  extra_context=None):
    context = {

    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@department_required
def department_invite_scientist(request, template='department/department_invite_scientist.html', extra_context=None):
    context = {

    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@department_required
def department_participant_list(request, template='department/department_participant_list.html', extra_context=None):
    scheme_list = CreditScheme.objects.filter(department=request.user)
    if not scheme_list:
        return HttpResponseRedirect(reverse_lazy('department_scheme'))

    scheme_id = request.GET.get('scheme_id', scheme_list[0].id)
    participant_list = ParticipantCreditScheme.objects.filter(credit_scheme__department=request.user,
                                                              credit_scheme__id=scheme_id)

    context = {
        'participant_list': participant_list,
        'scheme_list': scheme_list,
        'scheme_id': scheme_id,
        'scheme': scheme_list[0],
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@department_required
def department_scheme(request, template='department/department_scheme.html', extra_context=None):
    scheme = None
    if request.method == 'POST':
        form = DepartmentSchemeForm(data=request.POST, files=request.FILES)
        try:
            scheme = CreditScheme.objects.get(department=request.user)
        except CreditScheme.DoesNotExist:
            scheme = CreditScheme(department=request.user)
        if form.is_valid():
            scheme.name = form.cleaned_data['name']
            scheme.start = form.cleaned_data['start']
            scheme.end = form.cleaned_data['end']
            scheme.total_credit = form.cleaned_data['total_credit']
            scheme.save()
            success(request, _(u'Update scheme successful.'))
    else:
        try:
            scheme = CreditScheme.objects.get(department=request.user)
            initial = {
                'name': scheme.name,
                'start': scheme.start,
                'end': scheme.end,
                'total_credit': scheme.total_credit,
            }
            form = DepartmentSchemeForm(initial=initial)
        except CreditScheme.DoesNotExist:
            form = DepartmentSchemeForm()

    context = {
        'form': form,
        'scheme': scheme,
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@department_required
def department_scientist_list(request, template='department/department_scientist_list.html', extra_context=None):
    scheme_list = CreditScheme.objects.filter(department=request.user)
    if not scheme_list:
        return HttpResponseRedirect(reverse_lazy('department_scheme'))

    scheme_id = request.GET.get('scheme_id', scheme_list[0].id)
    scientist_list = ScientistCreditScheme.objects.filter(credit_scheme__department=request.user,
                                                          credit_scheme__id=scheme_id)

    context = {
        'scientist_list': scientist_list,
        'scheme_list': scheme_list,
        'scheme_id': scheme_id,
        'scheme': scheme_list[0],
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@department_required
def choose_scheme_location(request, scheme_id, template='department/choose_scheme_location.html', extra_context=None):
    scheme = get_object_or_404(CreditScheme, id=scheme_id, department=request.user)
    selected_location_id = scheme.university_department.id if scheme.university_department else None

    if request.method == 'POST':
        location_id = request.REQUEST.get('location_id', None)
        location = UniversityDepartment.objects.get(id=location_id)
        scheme.university_department = location
        scheme.save()
        return HttpResponseRedirect(reverse_lazy('department_scheme'))
    else:
        location_list = UniversityDepartment.objects.filter(user=request.user)

    context = {
        'location_list': location_list,
        'scheme_id': scheme_id,
        'selected_location_id': selected_location_id,
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@department_required
def choose_coordinator(request, scheme_id, template='department/choose_coordinator.html', extra_context=None):
    scheme = get_object_or_404(CreditScheme, id=scheme_id, department=request.user)
    user_list = UserProfile.objects.filter(is_department=True).exclude(user=request.user)
    selected_user_list = []
    for c in scheme.coordinatorcreditscheme_set.all():
        selected_user_list.append(c.coordinator.id)
    if request.method == 'POST':
        user_id_list = request.POST.getlist('user_id', [])
        new_selected_users = User.objects.filter(id__in=user_id_list, userprofile__is_department=True)
        scheme.coordinatorcreditscheme_set.all().delete()
        for user in new_selected_users:
            CoordinatorCreditScheme(coordinator=user, credit_scheme=scheme).save()
        return HttpResponseRedirect(reverse_lazy('department_scheme'))

    context = {
        'user_list': user_list,
        'selected_user_list': selected_user_list,
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@department_required
def add_scheme_location(request, scheme_id, template='department/add_scheme_location.html', extra_context=None):
    location = None
    if request.method == 'POST':
        location_id = request.REQUEST.get('location_id', None)
        form = DepartmentSchemeLocationForm(data=request.POST, files=request.FILES)
        try:
            location = UniversityDepartment.objects.get(id=location_id)
        except UniversityDepartment.DoesNotExist:
            location = UniversityDepartment(user=request.user)
        if form.is_valid():
            location.university = form.cleaned_data['university']
            location.department = form.cleaned_data['department']
            location.address = form.cleaned_data['address']
            location.lng = form.cleaned_data['lng']
            location.lat = form.cleaned_data['lat']
            location.save()
            success(request, _(u'Update location successful.'))
            return HttpResponseRedirect(reverse_lazy('choose_scheme_location', args=[scheme_id, ]))
    else:
        coord = get_location(request)

        initial = {
            'user': request.user,
            'university': '',
            'department': '',
            'address': '',
            'lng': coord['lng'],
            'lat': coord['lat'],
        }
        form = DepartmentSchemeLocationForm(initial=initial)

    context = {
        'form': form,
        'location': location,
        'scheme_id': scheme_id,
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@department_required
def remove_all_participant(request):
    scheme_id = request.POST.get('scheme_id')
    try:
        scheme = CreditScheme.objects.get(id=scheme_id, department=request.user)
        ParticipantCreditScheme.objects.filter(credit_scheme=scheme).delete()
        result = {'status': 'success'}
    except CreditScheme.DoesNotExist:
        result = {'status': 'fail', 'reason': 'The credit scheme does not exist.'}
    return json_result(request, result)


@login_required
@department_required
def remove_all_scientist(request):
    scheme_id = request.POST.get('scheme_id', department=request.user)
    try:
        scheme = CreditScheme.objects.get(id=scheme_id)
        ScientistCreditScheme.objects.filter(credit_scheme=scheme).delete()
        result = {'status': 'success'}
    except CreditScheme.DoesNotExist:
        result = {'status': 'fail', 'reason': 'The credit scheme does not exist.'}
    return json_result(request, result)


@login_required
@department_required
def choose_scientist(request, template='department/choose_scientist.html', extra_context=None):
    scientist_list = ScientistCreditScheme.objects.filter(credit_scheme__department=request.user)
    if scientist_list:
        selected_user_list = []
        for scientist in scientist_list:
            selected_user_list.append(scientist.scientist.id)
        user_list = User.objects.filter(userprofile__is_scientist=True).exclude(
            Q(id__in=selected_user_list) | Q(id=request.user.id))
    else:
        user_list = User.objects.filter(userprofile__is_scientist=True).exclude(id=request.user.id)
    scheme_list = CreditScheme.objects.filter(department=request.user)
    if request.method == 'POST':
        user_id_list = request.POST.getlist('user_id', [])
        scheme_id = request.POST.get('scheme_id', None)
        selected_user_list = User.objects.filter(id__in=user_id_list, userprofile__is_scientist=True)
        scheme = CreditScheme.objects.get(id=scheme_id)
        for user in selected_user_list:
            ScientistCreditScheme(scientist=user, credit_scheme=scheme).save()
        return HttpResponseRedirect(reverse_lazy('department_scientist_list'))

    context = {
        'user_list': user_list,
        'scheme_list': scheme_list,
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@department_required
def delete_scientist(request):
    try:
        scientist_id_list = request.POST.getlist('scientist_id', [])
        scheme_id = request.POST.get('scheme_id', None)

        scheme = get_object_or_404(CreditScheme, id=scheme_id, department=request.user)
        scientist_list = ScientistCreditScheme.objects.filter(id__in=scientist_id_list, credit_scheme=scheme)

        for scientist in scientist_list:
            scheme.remain_credit += scientist.remain_credit
            scheme.save()
            scientist.delete()

        result = {'status': 'success'}
    except Exception as e:
        result = {'status': 'fail', 'reason': e.message}
    return json_result(request, result)


@login_required
@department_required
def assign_credit(request):
    try:
        scheme_id = request.POST.get('scheme_id', None)
        scientist_id = request.POST.get('scientist_id', None)
        assigned_credit = int(request.POST.get('assigned_credit', 0))

        scheme = CreditScheme.objects.get(id=scheme_id)
        scientist = ScientistCreditScheme.objects.get(id=scientist_id, credit_scheme=scheme)
        add_assigned_credit = assigned_credit - scientist.assigned_credit
        if add_assigned_credit > scheme.remain_credit:
            result = {'status': 'fail', 'reason': 'not enough remain credit',
                      'scientist_assigned_credit': scientist.assigned_credit}
        elif assigned_credit <= scientist.assigned_credit:
            result = {'status': 'fail', 'reason': 'credit can not be reduced',
                      'scientist_assigned_credit': scientist.assigned_credit}
        else:
            scheme.remain_credit -= add_assigned_credit
            scheme.save()
            scientist.remain_credit += add_assigned_credit
            scientist.assigned_credit = assigned_credit
            scientist.save()
            result = {'status': 'success', 'scientist_remain_credit': scientist.remain_credit,
                      'scientist_assigned_credit': scientist.assigned_credit,
                      'scheme_remain_credit': scheme.remain_credit}
    except Exception as e:
        result = {'status': 'fail', 'reason': e.message}
    return json_result(request, result)


@login_required
@department_required
def choose_participant(request, template='department/choose_participant.html', extra_context=None):
    participant_list = ParticipantCreditScheme.objects.filter(credit_scheme__department=request.user)
    if participant_list:
        selected_user_list = []
        for participant in participant_list:
            selected_user_list.append(participant.participant.id)
        user_list = User.objects.filter(userprofile__is_participant=True).exclude(
            Q(id__in=selected_user_list) | Q(id=request.user.id))
    else:
        user_list = User.objects.filter(userprofile__is_participant=True).exclude(id=request.user.id)
    scheme_list = CreditScheme.objects.filter(department=request.user)
    if request.method == 'POST':
        user_id_list = request.POST.getlist('user_id', [])
        scheme_id = request.POST.get('scheme_id', None)
        selected_user_list = User.objects.filter(id__in=user_id_list, userprofile__is_participant=True)
        scheme = CreditScheme.objects.get(id=scheme_id)
        for user in selected_user_list:
            ParticipantCreditScheme(participant=user, credit_scheme=scheme).save()
        return HttpResponseRedirect(reverse_lazy('department_participant_list'))

    context = {
        'user_list': user_list,
        'scheme_list': scheme_list,
    }

    if extra_context:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
@department_required
def delete_participant(request):
    try:
        participant_id_list = request.POST.getlist('participant_id', [])
        ParticipantCreditScheme.objects.filter(id__in=participant_id_list,
                                               credit_scheme__department=request.user).delete()
        result = {'status': 'success'}
    except Exception as e:
        result = {'status': 'fail', 'reason': e.message}
    return json_result(request, result)


@login_required
@department_required
def set_required_credit(request):
    try:
        scheme_id = request.POST.get('scheme_id', None)
        participant_id = request.POST.get('participant_id', None)
        required_credit = int(request.POST.get('required_credit', 0))

        if required_credit > 0:
            participant = ParticipantCreditScheme.objects.get(id=participant_id, credit_scheme__id=scheme_id)
            if participant:
                space_required_credit = required_credit - participant.required_credit
                participant.required_credit = required_credit
                participant.incomplete_credit += space_required_credit
                participant.save()
                result = {'status': 'success', 'incomplete_credit': participant.incomplete_credit}
            else:
                result = {'status': 'fail', 'reason': 'participant does not exists'}
        else:
            result = {'status': 'fail', 'reason': 'required credit can not set to negative number'}
    except Exception as e:
        result = {'status': 'fail', 'reason': e.message}
    return json_result(request, result)


@csrf_exempt
def api_scientists(request):
    response_data = __get_user_data(request, USER_TYPE_SCIENTIST)
    return HttpResponse(json.dumps(response_data), mimetype='application/json')


@csrf_exempt
def api_participants(request):
    response_data = __get_user_data(request, USER_TYPE_PARTICIPANT)
    return HttpResponse(json.dumps(response_data), mimetype='application/json')


def __get_user_data(request, user_type):
    response_data = []
    q = request.REQUEST.get('q', None)

    if q:
        if user_type == USER_TYPE_SCIENTIST:
            scientist_list = User.objects.filter(Q(userprofile__is_scientist=True),
                                                 Q(username=q) | Q(email__icontains=q)).exclude(Q(id=request.user.id))
        elif user_type == USER_TYPE_PARTICIPANT:
            scientist_list = User.objects.filter(Q(userprofile__is_participant=True),
                                                 Q(username=q) | Q(email__icontains=q)).exclude(Q(id=request.user.id))

        for scientist in scientist_list:
            response_data.append(
                {
                    'id': scientist.id,
                    'avatar': avatar_url(scientist, 80),
                    'display_name': scientist.username,
                    'email': scientist.email
                }
            )
    return response_data