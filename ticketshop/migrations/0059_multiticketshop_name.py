# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2018-11-27 12:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketshop', '0058_auto_20181120_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='multiticketshop',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
    ]
