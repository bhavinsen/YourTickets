# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-04-06 14:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketshop', '0037_auto_20170406_0046'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='service_costs',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]