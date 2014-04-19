from django import template

from scientist.models import Research
from core.utils import get_location

register = template.Library()


@register.inclusion_tag('gmap/_mark_researches.html', takes_context=True)
def mark_researches(context, research_list=[], is_resize='false', width=None, height=400):
    request = context['request']
    location = get_location(request)
    context.update({
        'location': location,
        'research_list': research_list,
        'width': '%d%s' % (width, 'px') if width else '100%',
        'height': '%d%s' % (height, 'px'),
        'is_resize': is_resize
    })
    return context


@register.inclusion_tag('gmap/_mark_researches.html', takes_context=True)
def mark_all_researches(context, is_resize='false', width=None, height=400):
    request = context['request']
    location = get_location(request)
    research_list = Research.objects.filter(is_publish=True, is_complete=False)
    context.update({
        'location': location,
        'research_list': research_list,
        'width': '%d%s' % (width, 'px') if width else '100%',
        'height': '%d%s' % (height, 'px'),
        'is_resize': is_resize
    })
    return context