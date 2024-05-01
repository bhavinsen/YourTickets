from django import forms
from ticketshop.models import EventPayments
from youradmin.common.formwidgets.datetimepicker import DateTimePicker

class FinancialPaymentsForm(forms.ModelForm):
    # name = forms.CharField(max_length=100, required=True)
    amount = forms.DecimalField()
    description = forms.CharField(widget=forms.Textarea, required=False)
    payout_date = forms.DateTimeField(widget=DateTimePicker(
        format='%Y-%m-%d ',
        config={'sideBySide': False, 'format': 'YYYY-MM-DD'}
    ), label='Start time (optional)', required=False)
    type = forms.ChoiceField(widget=forms.Select, choices=EventPayments.TYPES)

    class Meta:
        model = EventPayments
        fields = ('payout_date', 'type', 'amount', 'description')