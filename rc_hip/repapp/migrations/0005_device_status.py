# Generated by Django 4.2 on 2023-05-29 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repapp', '0004_alter_onetimelogin_secret'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='status',
            field=models.IntegerField(default=0, verbose_name='Status'),
        ),
    ]
