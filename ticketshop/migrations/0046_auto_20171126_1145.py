# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-11-26 10:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticketshop', '0045_auto_20170727_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soldticket',
            name='guest_ticket',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ticketshop.GuestTickets'),
        ),
        migrations.AlterField(
            model_name='soldticket',
            name='primary_ticket',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ticketshop.SoldTicket'),
        ),
    ]