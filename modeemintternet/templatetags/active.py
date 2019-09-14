from re import search

from django import template

register = template.Library()


@register.simple_tag
def active(request, pattern):
    if search(pattern, request.path):
        return 'active'
    return ''
