from django import template
from yourtickets.common.form_utils import is_field_checkbox, is_field_dateinput, \
    is_field_clearablefileinput

register = template.Library()


@register.simple_tag(name='formDecorator')
def formDecorator(form, *args, **kwargs):

    default = 'youradmin/partials/form.html'
    template_name = kwargs.get('template_name', None)
    addButton = kwargs.get('addButton', False)
    buttonText = kwargs.get('buttonText', 'Save')

    tpl = template.loader.get_template(template_name or default)

    for key in form.fields:
        field = form.fields[key]
        if is_field_dateinput(field):
            field.widget.attrs['class'] = 'form-control ui-datepicker'
        elif is_field_clearablefileinput(field):
            field.widget.attrs['class'] = ''
        elif not is_field_checkbox(field):
            field.widget.attrs['class'] = 'form-control'

    return tpl.render({'form': form, 'button': addButton,'buttonText': buttonText,'data': kwargs})
