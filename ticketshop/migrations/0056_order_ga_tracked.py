# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2018-10-29 19:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketshop', '0055_userextra_terms_agreed'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ga_tracked',
            field=models.BooleanField(default=False),
        ),
    ]