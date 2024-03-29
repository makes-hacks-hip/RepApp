# Generated by Django 4.2 on 2023-08-27 19:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OneTimeLogin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secret', models.CharField(max_length=200, unique=True, verbose_name='Secret')),
                ('url', models.CharField(max_length=200, verbose_name='URL')),
                ('created', models.DateField(default=django.utils.timezone.now, verbose_name='Creation date')),
                ('login_used', models.BooleanField(default=False, verbose_name='Was the login used?')),
                ('login_date', models.DateField(null=True, verbose_name='Login date')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'One time login',
                'verbose_name_plural': 'One time logins',
            },
        ),
    ]
