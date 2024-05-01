from django import forms
from ticketshop.models import (UserExtra)
from PIL import Image
from django.conf import settings
import os


class RegisterForm(forms.Form):
    email = forms.EmailField(label='Username', max_length=200, required=True)
    # password = forms.CharField(label="Password", widget=forms.PasswordInput(), max_length=200, required=True)
    first_name = forms.CharField(label='First name', max_length=200, required=True)
    last_name = forms.CharField(label='Last name', max_length=200, required=True)


# saved in userExtraSeller
class BusinessInfoForm(forms.Form):
    place = forms.CharField(max_length=200, required=False)

    coc_number = forms.CharField(label='coc', max_length=200, required=False)
    tax_number = forms.CharField(label='btw', max_length=200, required=False)
    account_owner = forms.CharField(label='account_holder', max_length=200, required=False)
    account_number = forms.CharField(label='account_number', max_length=200, required=False)

    postal_code = forms.CharField(label='Last name', max_length=200, required=False)
    house_number = forms.CharField(label='Last name', max_length=200, required=False)
    house_number_addition = forms.CharField(label='Last name', max_length=200, required=False)
    company_name = forms.CharField(label='company name', max_length=200, required=False)
    big = forms.CharField(label='Last name', max_length=200, required=False)


# saved in userExtra
# if you are an organizer this is saved (which is horrible):
# userEx = UserExtra(
#                 user=user, birth_date='1970-01-01',
#                 adress='1111AA', sex='M', is_organizer=True, is_visitor=False,
#                 activate_token=token, terms_agreed=True
#
#             )
class AccountForm(forms.ModelForm):

    class Meta:
        model = UserExtra
        fields = ['avatar']

    def save(self, *args, **kwargs):
        # Save this photo instance first
        record = super(AccountForm, self).save(*args, **kwargs)

        try:
            image = Image.open(record.avatar)
            if image.width > 775:
                ratio = float(775) / float(image.width)
                size = 775, ratio * image.height
                image.thumbnail(size)
                extension = os.path.splitext(record.avatar.name)[1][1:]
                if extension.lower() == 'jpg':
                    extension = 'JPEG'
                image.save(settings.MEDIA_ROOT + '/' + record.avatar.name, extension, optimize=True)
        except Exception as e:
            print('some image save error')
            pass
