# Generated by Django 4.1.7 on 2023-04-24 20:54

import Apps.Eventos.models
import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Career',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(error_messages={'unique': 'Ya existe un registro con este nombre. Intente con otro.'}, max_length=150, unique=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(blank=True, null=True, upload_to=Apps.Eventos.models.event_directory_logo_path, validators=[django.core.validators.FileExtensionValidator(['jpeg', 'jpg'])])),
                ('title', models.CharField(max_length=150, unique=True)),
                ('place', models.CharField(max_length=150)),
                ('addressed_to', models.TextField(max_length=300)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('start_date', models.DateField()),
                ('final_date', models.DateField()),
                ('modality', models.CharField(choices=[('Presencial', 'Presencial'), ('Online', 'Online'), ('Online y Presencial', 'Online y Presencial')], max_length=20)),
                ('country_phone', django_countries.fields.CountryField(max_length=2)),
                ('phone', models.BigIntegerField()),
                ('alternative_phone', models.BigIntegerField(blank=True, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('alternative_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('link_to_classroom', models.URLField(null=True)),
                ('code_meeting', models.CharField(max_length=500, null=True)),
                ('platform_meeting', models.CharField(choices=[('', ''), ('Zoom', 'Zoom'), ('Google Meet', 'Google Meet'), ('Microsoft Teams', 'Microsoft Teams'), ('Discord', 'Discord'), ('Skype', 'Skype')], max_length=20, null=True)),
                ('event_planning', models.FileField(max_length=255, upload_to=Apps.Eventos.models.event_directory_planning_file_path, validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('link_video', models.URLField(blank=True, null=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('active', models.BooleanField(default=True)),
                ('certify', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'Events',
            },
        ),
        migrations.CreateModel(
            name='EventParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, editable=False, max_length=100, null=True, unique=True)),
                ('capture_id', models.CharField(blank=True, editable=False, max_length=100, null=True, unique=True)),
                ('client_name', models.CharField(max_length=150, null=True)),
                ('client_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('payer_id', models.CharField(blank=True, editable=False, max_length=100, null=True)),
                ('active', models.BooleanField(default=False)),
                ('total_buy', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('discount_paypal', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('net_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('status_buy', models.CharField(default='', max_length=15)),
                ('status_code', models.CharField(default='', max_length=100)),
                ('pay', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'EventParticipants',
            },
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(blank=True, default='user_profile_placeholder.jpg', null=True, upload_to=Apps.Eventos.models.participant_directory_image_path)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('country_of_birth', django_countries.fields.CountryField(max_length=2)),
                ('dni', models.BigIntegerField(error_messages={'unique': 'Ya exíste un participante con este número de identificación'}, unique=True)),
                ('passport_number', models.BigIntegerField(blank=True, error_messages={'unique': 'Ya exíste un participante con este pasaporte'}, null=True, unique=True)),
                ('gender', models.CharField(choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino')], max_length=15)),
                ('birthdate', models.DateField()),
                ('current_country', django_countries.fields.CountryField(max_length=2)),
                ('address', models.TextField(max_length=400)),
                ('phone', models.BigIntegerField()),
                ('email', models.EmailField(error_messages={'unique': 'Ya esxite un participante con este email'}, max_length=254, unique=True)),
                ('alternative_email', models.EmailField(blank=True, error_messages={'unique': 'Ya esxite un participante con este email alternativo'}, max_length=254, null=True, unique=True)),
                ('object', models.TextField(max_length=256)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'Participants',
            },
        ),
    ]
