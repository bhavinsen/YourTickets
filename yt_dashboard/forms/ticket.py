from django import forms
from django.forms import HiddenInput

from ticketshop.models import Event, EventPayments
from youradmin.common.formwidgets.datetimepicker import DateTimePicker
from dashboard.common.form import ModelForm, Form

class TicketForm(Form):

    name = forms.CharField(required=True)
    description = forms.CharField(required=False)
    price = forms.IntegerField(required=True)
    quantity = forms.IntegerField(required=True)
    start_date = forms.DateTimeField(required=True)
    end_date = forms.DateTimeField(required=True)
    max_sold = forms.IntegerField(required=True)
    person_amount = forms.IntegerField(required=True)

    # def clean(self):
    #
    #     cleaned_data = self.cleaned_data
    #     if 'end_date' in cleaned_data and 'start_date' in cleaned_data:
    #         if cleaned_data['end_date'] < cleaned_data['start_date']:
    #             # pass
    #             self.add_error('end_date', 'Eind datum kan niet voor de start datum')
    #             self.add_error('start_date', 'Start datum kan niet na de eind datum')
    #     return cleaned_data