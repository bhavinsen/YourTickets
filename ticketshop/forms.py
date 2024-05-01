from django import forms
from ticketshop.models import (
    UserExtra, SoldTicket
)

class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Emailadres"), max_length=254)

class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("De 2 velden komen niet overeen."),
        }
    new_password1 = forms.CharField(label=("Nieuw wachtwoord"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("Herhaal nieuw wachtwoord"),
                                    widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
        return password2

class SendTicketsToForm(forms.Form):
    # name = forms.CharField(max_length=100, required=True)
    email = forms.CharField(widget=forms.TextInput, required=True)
    first_name = forms.CharField(widget=forms.TextInput, required=True)
    last_name = forms.CharField(widget=forms.TextInput, required=True)

    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=(('M', 'Man'), ('F', 'Vrouw'), ('X', 'X')), required=True)

    def is_valid(self):
        ret = forms.Form.is_valid(self)
        for f_name in self.errors:
            classes = self.fields[f_name].widget.attrs.get('class', '')
            classes += ' error'
            self.fields[f_name].widget.attrs['class'] = classes
        return ret