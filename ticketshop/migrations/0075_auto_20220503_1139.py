# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-05-03 09:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketshop', '0074_order_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uid',
            field=models.CharField(blank=True, default='', max_length=32),
        ),
    ]
