# Generated by Django 5.0.4 on 2024-05-14 05:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transport_scolaire', '0006_assignationitineraire_bus_ecoleassignation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ecoleassignation',
            name='date_assignation',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
