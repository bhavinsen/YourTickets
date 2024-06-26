# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-29 20:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketshop', '0011_auto_20160726_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketshopcustom',
            name='bg_img',
            field=models.ImageField(default='static/images/event/bg.jpg', upload_to='static/images/event/'),
        ),
        migrations.AddField(
            model_name='ticketshopcustom',
            name='header_img',
            field=models.ImageField(default='static/images/event/header.jpg', upload_to='static/images/event/'),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateTimeField(blank=True, verbose_name='date ended'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateTimeField(blank=True, verbose_name='date started'),
        ),
        migrations.AlterField(
            model_name='userextra',
            name='birth_date',
            field=models.DateField(verbose_name='birth date'),
        ),
    ]
