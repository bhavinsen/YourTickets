import datetime

from django import forms

from ticketshop.models import Event
from dashboard.common.form import ModelForm, Form

class EventForm(Form):

    # ,

    start_date = forms.DateField(required=True, input_formats=['%d-%m-%Y'])
    start_time = forms.CharField(required=True)

    end_date = forms.DateField(required=True, input_formats=['%d-%m-%Y'])
    end_time = forms.CharField(required=True)

    description = forms.CharField(required=False)
    event_url = forms.CharField(required=False)
    location = forms.CharField(required=False)
    title = forms.CharField(required=True)
    show_covid19_info = forms.BooleanField(required=False)

    # class Meta:
    #     model = Event
    #     fields = ('id', 'title', 'location', 'description', 'start_date', 'end_date', 'event_url')

    # def __init__(self, *args, **kwargs):
    #     super(EventForm, self).__init__(*args, **kwargs)

        # if self.instance:
        #     from django.utils import timezone

            # start_time = timezone.localtime(self.instance.start_date).strftime('%H:%M')
            # end_time = timezone.localtime(self.instance.end_date).strftime('%H:%M')

            # self.fields['start_time'] = forms.CharField(required=True, initial=start_time)
            # self.fields['end_time'] = forms.CharField(required=True, initial=end_time)
        # elif kwargs.get('data'):
            # data = kwargs.get('data')
            # start_time = timezone.localtime(data.get('start_date')).strftime('%H:%M')
            # end_time = timezone.localtime(data.get('end_date')).strftime('%H:%M')
            #
            # self.fields['start_time'] = forms.CharField(required=True, initial=start_time)
            # self.fields['end_time'] = forms.CharField(required=True, initial=end_time)

        # else:
            # self.fields['start_time'] = forms.CharField(required=True)
            # self.fields['end_time'] = forms.CharField(required=True)

    # def clean(self):
    #
    #     cleaned_data = self.cleaned_data
    #     if 'end_date' in cleaned_data and 'start_date' in cleaned_data:
    #         if cleaned_data['end_date'] < cleaned_data['start_date']:
    #             # pass
    #             self.add_error('end_date', 'Eind datum kan niet voor de start datum')
    #             self.add_error('start_date', 'Begin datum kan niet na de start datum')
    #     return cleaned_data

    # def is_valid(self):
    #     ret = forms.ModelForm.is_valid(self)
    #     for f_name in self.errors:
    #         if f_name == 'end_date' or f_name == 'start_date':
    #             classes = self.fields[f_name].widget.attrs.get('class', '')
    #             classes += ' form-error'
    #             self.fields[f_name].widget.attrs['class'] = classes
    #         else:
    #             classes = self.fields[f_name].widget.attrs.get('class', '')
    #             classes += ' form-error'
    #             self.fields[f_name].widget.attrs['class'] = classes
    #     return ret