# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-25 20:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketshop', '0009_ticketshopcustom'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=1000)),
            ],
        ),
    ]
