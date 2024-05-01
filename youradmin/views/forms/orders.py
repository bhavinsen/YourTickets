from django import forms

class ResendTicketsForm(forms.Form):
    email = forms.CharField(max_length=100, required=True)
