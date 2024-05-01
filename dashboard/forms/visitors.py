from django import forms

from ticketshop.models import Event
from dashboard.common.form import ModelForm, Form

class SendticketForm(Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.xlsx', '.xls']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')

class GuestlistUploadForm(Form):
    importfile = forms.FileField(validators=[validate_file_extension])