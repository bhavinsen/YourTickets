# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-30 16:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticketshop', '0013_auto_20160729_2238'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_paid', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Order creation date')),
            ],
        ),
        migrations.AddField(
            model_name='soldticket',
            name='order_nr',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ticketshop.Order'),
        ),
    ]
