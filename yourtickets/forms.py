from django import forms

class RegisterForm(forms.Form):
    username = forms.EmailField(label='Username', max_length=200, required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput(), max_length=200, required=True)
    first_name = forms.CharField(label='First name', max_length=200, required=True)
    last_name = forms.CharField(label='Last name', max_length=200, required=True)


