import os

from PIL import Image
from django import forms
from django.conf import settings
from django import forms
from django.forms import HiddenInput

from ticketshop.models import (TicketShopCustom)
from youradmin.common.formwidgets.selectpicker import SelectPicker
from ticketshop.models import DynamicUrl


class TicketShopCustomFormNew(forms.ModelForm):

    class Meta:
        model = TicketShopCustom
        fields = ['event_id', 'primary_color', 'secondary_color', 'header_img', 'bg_img']

    def save(self, *args, **kwargs):
        # Save this photo instance first
        record = super(TicketShopCustomFormNew, self).save(*args, **kwargs)

        try:
            image = Image.open(record.header_img)
            if image.width > 775:
                ratio = float(775)/float(image.width)
                size = 775, ratio*image.height
                image.thumbnail(size)
                extension = os.path.splitext(record.bg_img.name)[1][1:]
                if extension.lower() == 'jpg':
                    extension = 'JPEG'
                image.save(settings.MEDIA_ROOT+'/'+record.header_img.name, extension, optimize=True)
        except Exception as e:
             pass

        try:
            image = Image.open(self.cleaned_data['bg_img'])
            # import pdb;pdb.set_trace()
            if image.width > 1000:
                # print(record.bg_img.name)
                ratio = float(1000) / float(image.width)
                size = 1000, ratio * image.height
                image.thumbnail(size)
                extension = os.path.splitext(record.bg_img.name)[1][1:]
                if extension.lower() == 'jpg':
                    extension = 'JPEG'
                image.save(settings.MEDIA_ROOT + '/' + record.bg_img.name, extension, optimize=True)
        except Exception as e:
            pass