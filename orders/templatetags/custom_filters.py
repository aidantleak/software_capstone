from django import template

register = template.Library()
@register.filter
def beautify_status(value):
    """Converts underscores to spaces and capitalizes each word."""
    return value.replace('_', ' ').title()


