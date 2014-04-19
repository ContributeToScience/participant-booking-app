from django import template
from scientist.models import Research

register = template.Library()


@register.simple_tag
def get_distance(request, research):
    if request and research:
        research = Research.objects.get(id=research.id)
        return research.get_distance(request)
    return 0