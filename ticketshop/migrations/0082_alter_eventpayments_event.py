# Generated by Django 3.2.3 on 2022-08-07 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticketshop', '0081_auto_20220807_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpayments',
            name='event',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ticketshop.event'),
        ),
    ]