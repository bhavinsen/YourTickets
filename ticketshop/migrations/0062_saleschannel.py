# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2019-01-16 15:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticketshop', '0061_auto_20181211_1312'),
    ]

    operations = [
        migrations.CreateModel(
            name='Saleschannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200)),
                ('url_name', models.CharField(default='', max_length=100)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticketshop.Event')),
            ],
        ),
    ]