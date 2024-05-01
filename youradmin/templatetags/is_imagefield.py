from django import template

from yourtickets.common.form_utils import is_field_imagefield

register = template.Library()


@register.filter(name='is_imagefield')
def is_imagefield(field):
    return is_field_imagefield(field.field)
