from django import forms

from dashboard.common.form import ModelForm, Form


class LineupForm(Form):
    artist = forms.CharField(required=True)
