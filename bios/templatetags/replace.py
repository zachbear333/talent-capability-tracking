from django import template
import re

register = template.Library()
@register.filter(name='replace')
def replace(value):
    return re.sub("[_]+", " ", value)

@register.filter(name="remove_par")
def remove_par(value):
    value = value.replace('(', '')
    value = value.replace(')', '')
    return value

@register.filter(name="my_split")
def my_split(value):
    return value.replace(' ', '_')

@register.filter(name='ifinlist')
def ifinlist(value, list):
    return value in list