from django import template

register = template.Library()

@register.filter
def times(value, arg):
    try:
        return value * arg
    except (TypeError, ValueError):
        return value  # Returns the original value if multiplication fails
