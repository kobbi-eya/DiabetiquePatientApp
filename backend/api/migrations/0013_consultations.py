# Generated by Django 5.0.4 on 2024-04-20 02:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_alter_patient_idmed'),
    ]

    operations = [
        migrations.CreateModel(
            name='consultations',
            fields=[
                ('idconsultations', models.AutoField(primary_key=True, serialize=False)),
                ('date_consultation', models.DateField(default='')),
                ('heure_consultation', models.TimeField(default=None)),
                ('ordonnance', models.TextField(default='')),
                ('description', models.TextField(default='')),
                ('bilan', models.TextField(default='')),
                ('idmede', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.medecin')),
                ('idpat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.patient')),
            ],
        ),
    ]
