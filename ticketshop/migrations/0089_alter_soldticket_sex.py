# Generated by Django 3.2.3 on 2023-03-01 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketshop', '0088_prereg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soldticket',
            name='sex',
            field=models.CharField(choices=[('M', 'Man'), ('F', 'Vrouw'), ('X', 'X')], default='N', max_length=1),
        ),
    ]
