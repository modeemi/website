from django.conf import settings
from django import template

register = template.Library()


@register.simple_tag
def version():
    return settings.VERSION
