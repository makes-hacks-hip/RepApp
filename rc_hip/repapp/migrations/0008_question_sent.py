# Generated by Django 4.2 on 2023-05-29 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repapp', '0007_question_open'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='sent',
            field=models.BooleanField(default=False, verbose_name='gesendet'),
        ),
    ]
