# Generated by Django 4.2 on 2023-04-23 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repapp', '0012_remove_device_secret_remove_guest_confirmed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cafe',
            name='address',
            field=models.CharField(max_length=200, verbose_name='Adresse'),
        ),
        migrations.AlterField(
            model_name='device',
            name='device',
            field=models.CharField(max_length=200, verbose_name='Art des Geräts'),
        ),
        migrations.AlterField(
            model_name='device',
            name='error',
            field=models.TextField(verbose_name='Fehlerbeschreibung'),
        ),
        migrations.AlterField(
            model_name='device',
            name='manufacturer',
            field=models.CharField(max_length=200, verbose_name='Hersteller & Modell/Typ'),
        ),
    ]
