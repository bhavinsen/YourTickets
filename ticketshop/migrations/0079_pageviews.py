# Generated by Django 3.2.3 on 2022-07-28 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticketshop', '0078_auto_20220718_1813'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageViews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(default='', max_length=200)),
                ('ip', models.CharField(default='', max_length=200)),
                ('url', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('event_id', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ticketshop.event')),
            ],
        ),
    ]