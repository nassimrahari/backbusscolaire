# Generated by Django 5.0.4 on 2024-06-21 13:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transport_scolaire', '0008_anneeinscription_remove_assignationitineraire_eleve_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inscription',
            name='eleve',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='transport_scolaire.eleve'),
        ),
    ]