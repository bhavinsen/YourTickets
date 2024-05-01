import json
from django.forms.widgets import DateTimeBaseInput
from django.utils.encoding import force_text
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string


class DateTimePicker(DateTimeBaseInput):

    def __init__(self, *args, **kwargs):

        self.config = kwargs.pop('config', {})

        super(DateTimePicker, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''
        
        final_attrs = self.build_attrs(base_attrs=attrs, extra_attrs={'type':self.input_type, 'name':name})
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self.format_value(value))

        return render_to_string('youradmin/partials/formwidgets/datetimepicker.html', {
            'input_attrs': final_attrs,
            'config_attrs': json.dumps(self.config),
            'dateid': get_random_string(length=10)
        })
