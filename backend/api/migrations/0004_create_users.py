from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]
    operations = [
        migrations.CreateModel(
            name='users',
            fields=[
                ('idusers', models.AutoField(primary_key=True)),
                ('password', models.CharField(max_length=255)),
                ('nom', models.CharField(default='', max_length=50)),
                ('prenom', models.CharField(default='', max_length=50)),
                ('role', models.CharField(choices=[('MEDECIN', 'Médecin'), ('PATIENT', 'Patient')], default='', max_length=10)),
                ('email', models.CharField(default='', max_length=50, unique=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]