from django import template


register = template.Library()

@register.filter
def beautify_status(value):
    """Converts underscores to spaces and capitalizes each word."""
    return value.replace('_', ' ').title()


import re
from django import template

register = template.Library()

@register.filter
def phone_format(value):
    digits = re.sub(r'\D', '', str(value))
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return value
