from django import template

register = template.Library()

@register.filter(name='beautify_status')
def beautify_status(value):
    return value.replace('_', ' ').title()