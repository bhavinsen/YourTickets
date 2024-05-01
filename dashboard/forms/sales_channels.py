from django import forms


class SalesChannelForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput, label='Name')
    # url_name = forms.CharField(widget=forms.TextInput, label='Url name')
    # event = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):

        # event_id = kwargs.pop('event_id', None)

        super(SalesChannelForm, self).__init__(*args, **kwargs)

        # self.fields['event'].initial = event_id
