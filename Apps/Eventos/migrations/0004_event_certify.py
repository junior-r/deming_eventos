# Generated by Django 4.1.5 on 2023-03-26 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eventos', '0003_event_link_to_classroom'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='certify',
            field=models.BooleanField(default=False),
        ),
    ]
