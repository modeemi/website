from django import template
from modeemintternet.settings import VERSION_NUMBER

register = template.Library()

@register.simple_tag
def version():
    return VERSION_NUMBER
