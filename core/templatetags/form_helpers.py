from django import template
from django.forms import BoundField

register = template.Library()

@register.filter
def get_field_label(form, field_name):
    """
    Get the human-readable label for a form field.
    """
    if field_name in form.fields:
        field = form.fields[field_name]
        return field.label if field.label else field_name.replace('_', ' ').title()
    return field_name.replace('_', ' ').title()

