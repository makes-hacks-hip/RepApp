# Generated by Django 4.2 on 2023-08-29 11:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import email_interface.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='File name')),
                ('mime_type', models.CharField(max_length=200, verbose_name='MIME type')),
                ('file', models.FileField(null=True, upload_to=email_interface.models.attachment_file_path, verbose_name='File')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(max_length=200, verbose_name='Summary')),
                ('html_content', models.TextField(verbose_name='HTML content')),
                ('text_content', models.TextField(verbose_name='Text content')),
                ('created', models.DateField(default=django.utils.timezone.now, verbose_name='Creation date')),
                ('attachments', models.ManyToManyField(null=True, to='email_interface.attachment', verbose_name='Attachments')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('reply_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='email_interface.message', verbose_name='Reply to')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
        ),
    ]