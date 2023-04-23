# Generated by Django 4.2 on 2023-04-23 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repapp_users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'Benutzer', 'verbose_name_plural': 'Benutzer'},
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='eMail Adresse'),
        ),
    ]
