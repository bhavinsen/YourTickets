# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-30 16:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketshop', '0014_auto_20160730_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
