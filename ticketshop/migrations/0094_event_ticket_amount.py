# Generated by Django 3.2.3 on 2023-06-26 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketshop', '0093_auto_20230615_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='ticket_amount',
            field=models.IntegerField(default=0),
        ),
    ]
