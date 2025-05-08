from django import template

import re


register = template.Library()

@register.filter(name='beautify_status')
def beautify_status(value):
    """Converts underscores to spaces and capitalizes each word."""
    return value.replace('_', ' ').title()


@register.filter
def phone_format(value):
    digits = re.sub(r'\D', '', str(value))
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return value
