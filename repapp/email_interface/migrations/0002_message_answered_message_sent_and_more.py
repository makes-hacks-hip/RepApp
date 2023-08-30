# Generated by Django 4.2 on 2023-08-29 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_interface', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='answered',
            field=models.BooleanField(default=False, verbose_name='answered?'),
        ),
        migrations.AddField(
            model_name='message',
            name='sent',
            field=models.BooleanField(default=False, verbose_name='sent?'),
        ),
        migrations.AlterField(
            model_name='message',
            name='attachments',
            field=models.ManyToManyField(to='email_interface.attachment', verbose_name='Attachments'),
        ),
    ]
