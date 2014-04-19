from django import template
from scientist.models import ScientistResearch

register = template.Library()

SCIENTIST_NAME_CACHE = {}
SCIENTIST_ID_CACHE = {}


@register.simple_tag
def get_scientist_name(research):
    scientist_name = ''
    global SCIENTIST_NAME_CACHE
    if research:
        if research.id in SCIENTIST_NAME_CACHE:
            scientist_name = SCIENTIST_NAME_CACHE[research.id]
        else:
            scientist_research = ScientistResearch.objects.get(research__id=research.id)
            scientist_name = scientist_research.scientist.userprofile.get_full_name()
            SCIENTIST_NAME_CACHE[research.id] = scientist_name
    return scientist_name


@register.simple_tag
def get_scientist_id(research):
    scientist_id = ''
    global SCIENTIST_ID_CACHE
    if research:
        if research.id in SCIENTIST_ID_CACHE:
            scientist_id = SCIENTIST_ID_CACHE[research.id]
        else:
            scientist_research = ScientistResearch.objects.get(research__id=research.id)
            scientist_id = scientist_research.scientist.id
            SCIENTIST_ID_CACHE[research.id] = scientist_id
    return scientist_id


@register.filter
def get_scientist_id(research):
    scientist_id = ''
    global SCIENTIST_ID_CACHE
    if research:
        if research.id in SCIENTIST_ID_CACHE:
            scientist_id = SCIENTIST_ID_CACHE[research.id]
        else:
            scientist_research = ScientistResearch.objects.get(research__id=research.id)
            scientist_id = scientist_research.scientist.id
            SCIENTIST_ID_CACHE[research.id] = scientist_id
    return scientist_id