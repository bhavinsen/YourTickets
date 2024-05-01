from django import template

from yourtickets.common.form_utils import is_field_checkbox

register = template.Library()


@register.filter(name='is_checkbox')
def is_checkbox(field):
    return is_field_checkbox(field.field)
