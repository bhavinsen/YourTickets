# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-11-17 13:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticketshop', '0026_auto_20161117_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dictionary',
            name='language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ticketshop.Languages'),
        ),
    ]
