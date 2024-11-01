# Generated by Django 5.0.4 on 2024-04-14 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='users',
            fields=[
                ('idusers', models.AutoField(primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=255)),
                ('nom', models.CharField(default='', max_length=50)),
                ('prenom', models.CharField(default='', max_length=50)),
                ('role', models.CharField(choices=[('MEDECIN', 'Médecin'), ('PATIENT', 'Patient')], default='', max_length=10)),
                ('email', models.CharField(default='', max_length=50, unique=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
