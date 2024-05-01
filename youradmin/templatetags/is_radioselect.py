from django import template

from yourtickets.common.form_utils import is_field_radioselect

register = template.Library()


@register.filter(name='is_radioselect')
def is_radioselect(field):
    return is_field_radioselect(field.field)
