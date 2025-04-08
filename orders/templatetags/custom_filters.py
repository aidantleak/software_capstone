from django import template

register = template.Library()

<<<<<<< HEAD
@register.filter(name='beautify_status')
def beautify_status(value):
    return value.replace('_', ' ').title()
=======
@register.filter
def beautify_status(value):
    """Converts underscores to spaces and capitalizes each word."""
    return value.replace('_', ' ').title()


