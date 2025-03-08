from django import template

register = template.Library()

@register.filter
def endswith(value, arg):
    """Return True if 'value' (string) ends with 'arg' (string)."""
    if not isinstance(value, str):
        return False
    return value.endswith(arg)
