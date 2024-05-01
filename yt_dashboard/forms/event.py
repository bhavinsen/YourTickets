from django import forms

from ticketshop.models import Event, EventPayments
from youradmin.common.formwidgets.datetimepicker import DateTimePicker
from dashboard.common.form import ModelForm, Form


class FinancialPaymentsForm(forms.ModelForm):
    # name = forms.CharField(max_length=100, required=True)
    amount = forms.DecimalField()
    description = forms.CharField(widget=forms.Textarea)
    payout_date = forms.DateTimeField(widget=DateTimePicker(
        format='%Y-%m-%d H:M:S',
        config={'sideBySide': True, 'format': 'YYYY-MM-DD HH:mm:ss'}
    ), label='Start time (optional)', required=False)


    class Meta:
        model = EventPayments
        fields = ('payout_date', 'amount', 'description')


class EventGeneralForm(Form):
    start_date = forms.DateTimeField(required=False)
    end_date = forms.DateTimeField(required=False)

    description = forms.CharField(required=False)
    event_url = forms.CharField(required=False)
    location = forms.CharField(required=False)
    title = forms.CharField(required=True)
    show_covid19_info = forms.BooleanField(required=False)
    online = forms.BooleanField(required=False)


    def clean(self):

        cleaned_data = self.cleaned_data
        if 'end_date' in cleaned_data and 'start_date' in cleaned_data:
            if cleaned_data['end_date'] < cleaned_data['start_date']:
                # pass
                self.add_error('end_date', 'Eind datum kan niet voor de start datum')
                self.add_error('start_date', 'Start datum kan niet na de eind datum')
        return cleaned_data