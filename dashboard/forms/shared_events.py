from django import forms


class SharedEventsForm(forms.Form):
    event = forms.CharField(widget=forms.HiddenInput, label='event')
    user = forms.CharField(widget=forms.TextInput, label='Email')

    def __init__(self, *args, **kwargs):

        # event_id = kwargs.pop('event_id', None)

        super(SharedEventsForm, self).__init__(*args, **kwargs)

        # self.fields['event'].initial = event_id

class TempSharedEventsForm(forms.Form):
    event = forms.CharField(widget=forms.HiddenInput, label='event')
    user_email = forms.CharField(widget=forms.TextInput, label='Email')

    def __init__(self, *args, **kwargs):

        # event_id = kwargs.pop('event_id', None)

        super(TempSharedEventsForm, self).__init__(*args, **kwargs)

        # self.fields['event'].initial = event_id