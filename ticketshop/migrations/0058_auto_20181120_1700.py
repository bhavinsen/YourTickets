# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2018-11-20 16:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticketshop', '0057_event_removed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Multiticketshop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organiser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticketshop.EventOrganiser')),
            ],
        ),
        migrations.CreateModel(
            name='MultiticketshopEvents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticketshop.Event')),
                ('multiticketshop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticketshop.Multiticketshop')),
            ],
        ),
        migrations.AddField(
            model_name='dynamicurl',
            name='type',
            field=models.CharField(choices=[('EVENT', 'Event'), ('MULTITICKETSHOP', 'Multi ticket shop')], default='EVENT', max_length=50),
        ),
        migrations.AlterField(
            model_name='dynamicurl',
            name='event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ticketshop.Event'),
        ),
        migrations.AddField(
            model_name='dynamicurl',
            name='multiticketshop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ticketshop.Multiticketshop'),
        ),
    ]