# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2018-12-04 15:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ticketshop', '0059_multiticketshop_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='multiticketshop',
            name='organiser',
        ),
        migrations.AddField(
            model_name='multiticketshop',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]