# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2018-09-21 07:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketshop', '0054_order_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='userextra',
            name='terms_agreed',
            field=models.BooleanField(default=False),
        ),
    ]
