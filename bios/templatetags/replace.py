from django import template
import re

register = template.Library()
@register.filter(name='replace')
def replace(value):
    return re.sub("[_]+", " ", value)