# Generated by Django 4.2.1 on 2023-05-09 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eventos', '0002_participant_how_did_you_find_out'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='url',
            field=models.URLField(default='https://example.com'),
            preserve_default=False,
        ),
    ]
