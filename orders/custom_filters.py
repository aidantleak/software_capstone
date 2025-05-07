from django import template
import re

register = template.Library()

@register.filter
def replace(value, args):
    old, new = args.split(',')
    return value.replace(old, new)

