# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-07-23 14:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticketshop', '0043_dynamicurl'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuestTickets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticketshop.Event')),
            ],
        ),
        migrations.AddField(
            model_name='soldticket',
            name='is_guest_ticket',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='soldticket',
            name='is_special_guest_ticket',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='soldticket',
            name='ticket_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ticketshop.Ticket'),
        ),
        migrations.AddField(
            model_name='soldticket',
            name='guest_ticket',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ticketshop.GuestTickets'),
        ),
    ]
