# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-11-26 11:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticketshop', '0046_auto_20171126_1145'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventPayments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payout_date', models.DateTimeField(blank=True, verbose_name=b'date sold')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('description', models.CharField(default=b'', max_length=200)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticketshop.Event')),
            ],
        ),
    ]
