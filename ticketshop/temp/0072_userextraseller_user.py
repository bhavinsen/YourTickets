# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-10-20 14:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ticketshop', '0071_order_agreed_covid19_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='userextraseller',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
