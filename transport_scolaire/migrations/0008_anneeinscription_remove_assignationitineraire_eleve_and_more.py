# Generated by Django 5.0.4 on 2024-06-21 12:09

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transport_scolaire', '0007_alter_ecoleassignation_date_assignation'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AnneeInscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annee', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='assignationitineraire',
            name='eleve',
        ),
        migrations.RemoveField(
            model_name='eleve',
            name='classe',
        ),
        migrations.RemoveField(
            model_name='eleve',
            name='date_inscription',
        ),
        migrations.RemoveField(
            model_name='eleve',
            name='etat',
        ),
        migrations.RemoveField(
            model_name='eleve',
            name='lieu_ramassage',
        ),
        migrations.RemoveField(
            model_name='eleve',
            name='lieu_remisage',
        ),
        migrations.RemoveField(
            model_name='eleve',
            name='ligne',
        ),
        migrations.RemoveField(
            model_name='eleve',
            name='montant_frais',
        ),
        migrations.RemoveField(
            model_name='eleve',
            name='type_inscription',
        ),
        migrations.RemoveField(
            model_name='eleve',
            name='user',
        ),
        migrations.CreateModel(
            name='Inscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_inscription', models.DateField(default=datetime.date.today)),
                ('type_inscription', models.CharField(choices=[('ramasse et remisage', 'Ramasse et Remisage'), ('ramassage', 'Ramassage'), ('remisage', 'Remisage')], default='ramassage', max_length=50)),
                ('montant_frais', models.DecimalField(blank=True, decimal_places=2, max_digits=10, max_length=50, null=True)),
                ('etat', models.CharField(default='en_attente', max_length=50)),
                ('annee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transport_scolaire.anneeinscription')),
                ('classe', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='transport_scolaire.classe')),
                ('lieu_ramassage', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='transport_scolaire.lieuramassage', verbose_name='lieu de ramassage')),
                ('lieu_remisage', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='eleves', to='transport_scolaire.lieuramassage', verbose_name='lieu de remisage')),
                ('ligne', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='transport_scolaire.ligne')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='assignationitineraire',
            name='inscription',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='transport_scolaire.inscription'),
        ),
    ]