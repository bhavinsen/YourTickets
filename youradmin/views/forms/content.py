from django import forms
from django.forms import HiddenInput

from youradmin.common.formwidgets.selectpicker import SelectPicker
from ticketshop.models import DynamicUrl

class EventUrlForm(forms.ModelForm):
    class Meta:
        model = DynamicUrl
        fields = ('event', 'multiticketshop', 'url_name', 'enabled', 'type')

        widgets = {
            'event': SelectPicker,
            'multiticketshop': SelectPicker,
            'type': HiddenInput
        }