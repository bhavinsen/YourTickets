# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-03-09 17:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticketshop', '0072_sharedevents'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempSharedEvents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_email', models.CharField(default='', max_length=200)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticketshop.Event')),
            ],
        ),
    ]
