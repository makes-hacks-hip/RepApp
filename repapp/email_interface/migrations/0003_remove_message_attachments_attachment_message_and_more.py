# Generated by Django 4.2 on 2023-08-30 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import email_interface.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('email_interface', '0002_message_answered_message_sent_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='attachments',
        ),
        migrations.AddField(
            model_name='attachment',
            name='message',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='email_interface.message', verbose_name='Message'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attachment',
            name='file',
            field=models.FileField(null=True, unique=True, upload_to=email_interface.models.attachment_file_path, verbose_name='File'),
        ),
        migrations.AlterField(
            model_name='message',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL, verbose_name='Receiver'),
        ),
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL, verbose_name='Sender'),
        ),
    ]
