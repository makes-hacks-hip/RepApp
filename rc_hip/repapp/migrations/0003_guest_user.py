# Generated by Django 4.2 on 2023-04-25 07:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repapp', '0002_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Benutzer'),
        ),
    ]