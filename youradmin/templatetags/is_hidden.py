from django import template

from yourtickets.common.form_utils import is_field_hidden

register = template.Library()


@register.filter(name='is_hidden')
def is_hidden(field):
    return is_field_hidden(field.field)
