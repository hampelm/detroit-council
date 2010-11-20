from django.template.loader import get_template
from django.template.defaultfilters import stringfilter
import string
from django import template
register = template.Library()

@register.filter
@stringfilter
def fake_slug(string):
    '''
    returns a fake slug for URL handling
    '''
    string = string.replace(" ", "_")
    string = string.replace("/", "-")
    return string

@register.filter
def hash(h, key):
    return h[key]