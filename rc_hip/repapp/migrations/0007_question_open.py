# Generated by Django 4.2 on 2023-05-29 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repapp', '0006_alter_question_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='open',
            field=models.BooleanField(default=True, verbose_name='offen'),
        ),
    ]
