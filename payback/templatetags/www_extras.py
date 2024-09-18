from django import template

register = template.Library()


@register.filter
def boolean_text(value):
    """
    Converts booleans to text
    """
    if bool(value):
        return "Yes"
    return "No"
