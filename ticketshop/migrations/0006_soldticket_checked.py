# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-19 12:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketshop', '0005_auto_20160513_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='soldticket',
            name='checked',
            field=models.BooleanField(default=False),
        ),
    ]
