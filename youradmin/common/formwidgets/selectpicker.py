import json

from django.forms.widgets import Select
from django.template.loader import render_to_string


class SelectPicker(Select):
    # template_name = 'youradmin/formwidgets/select_picker.html'

    def render(self, name, value, attrs=None, choices=None,  renderer=None):
        return render_to_string('youradmin/partials/formwidgets/select_picker.html', {
            'choices': self.choices,
            'name': name,
            'value': value,
            'attrs': attrs,
            'initial_data': json.dumps(value)
        })

    # def get_context(self, name, value, attrs):
    #     # context = super().get_context(name, value, attrs)
    #     super(SelectPicker, self).get_context(name, value, attrs)
    #
    #     attrs.update(self.attrs)
    #     context.update({
    #         'choices': self.choices,
    #         'name': name,
    #         'value': value,
    #         'attrs': attrs,
    #         'initial_data': json.dumps(value)
    #     })
    #     return context
