# Generated by Django 4.1.5 on 2023-03-14 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eventos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='career',
            name='name',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]