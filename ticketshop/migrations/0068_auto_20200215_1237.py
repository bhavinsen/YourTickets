# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2020-02-15 11:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketshop', '0067_orderlog_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderlog',
            name='type',
            field=models.CharField(choices=[('BEFORE_MOLLIE_AANVRAAG', 'BEFORE_MOLLIE_AANVRAAG'), ('WEBHOOK_MOLLIE_API_RECEIVED', 'WEBHOOK_MOLLIE_API_RECEIVED'), ('WEBHOOK_MOLLIE_ORDER_OK', 'WEBHOOK_MOLLIE_ORDER_OK'), ('WEBHOOK_MOLLIE_API_ERROR', 'WEBHOOK_MOLLIE_API_ERROR'), ('WEBHOOK_MOLLIE_EXCEPTION', 'WEBHOOK_MOLLIE_EXCEPTION'), ('WEBHOOK_MOLLIE_OK', 'WEBHOOK_MOLLIE_OK'), ('MAIL_PDF_CREATED', 'MAIL_PDF_CREATED'), ('MAIL_PDF_ERROR', 'MAIL_PDF_ERROR'), ('TYPE_MAIL_SEND', 'TYPE_MAIL_SEND'), ('TYPE_DONE', 'TYPE_DONE')], default='UNKNOWN', max_length=50),
        ),
    ]
