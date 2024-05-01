# Generated by Django 3.2.3 on 2022-08-07 19:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ticketshop', '0082_alter_eventpayments_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpayments',
            name='user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
