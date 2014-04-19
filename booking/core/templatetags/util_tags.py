from django import template

register = template.Library()


@register.simple_tag
def subtract(value, arg=0):
    return value - arg