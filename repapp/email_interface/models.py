import os
import logging
import django.utils.timezone
import django.dispatch
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


logger = logging.getLogger(__name__)


class Message(models.Model):
    """
    A email message.
    """
    summary = models.CharField(max_length=200, verbose_name=_(
        "Summary"), null=False)
    html_content = models.TextField(verbose_name=_("HTML content"), null=False)
    text_content = models.TextField(verbose_name=_("Text content"), null=False)
    created = models.DateField(verbose_name=_(
        "Creation date"), default=django.utils.timezone.now)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 null=True, verbose_name=_("Receiver"), related_name='receiver')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               null=True, verbose_name=_("Sender"), related_name='sender')
    reply_to = models.ForeignKey(
        'self', null=True, on_delete=models.SET_NULL, verbose_name=_("Reply to"))
    sent = models.BooleanField(verbose_name=_("sent?"), default=False)
    answered = models.BooleanField(verbose_name=_("answered?"), default=False)

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

    def __str__(self):
        return f'Message for user {self.receiver} with summary {self.summary}'

    def attachments(self):
        return Attachment.objects.filter(message=self).all()

    def thread(self):
        messages = [self]

        m = self
        while m.reply_to:
            messages.append(m.reply_to)
            m = m.reply_to

        messages.reverse()

        return messages

    def answers(self):
        return Message.objects.filter(reply_to=self).all()

    def siblings(self):
        if self.reply_to:
            return Message.objects.filter(reply_to=self.reply_to).all().exclude(pk=self.pk)
        else:
            return []

    @staticmethod
    def to_user(user):
        return Message.objects.filter(receiver=user).all()

    @staticmethod
    def from_user(user):
        return Message.objects.filter(sender=user).all()


def attachment_file_path(instance, filename):
    return f'{instance.owner.username}/{filename}'


class Attachment(models.Model):
    """
    A email attachment.
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, verbose_name=_("Owner"))
    name = models.CharField(max_length=200, verbose_name=_(
        "File name"), null=False)
    mime_type = models.CharField(max_length=200, verbose_name=_(
        "MIME type"), null=False)
    file = models.FileField(upload_to=attachment_file_path,
                            null=True, verbose_name=_("File"), unique=True)
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, null=False, verbose_name=_("Message"))

    class Meta:
        verbose_name = _('Attachment')
        verbose_name_plural = _('Attachments')

    def __str__(self):
        return f'Attachment {self.file} for {self.message}'

    def get_absolute_url(self):
        return f'{settings.MEDIA_URL}{self.file}'

    @staticmethod
    def of_user(user):
        return Attachment.objects.filter(owner=user).all()


@receiver(models.signals.post_delete, sender=Attachment)
def auto_delete_file_on_delete(sender, instance, **kwargs):  # pragma: no cover
    # manual test was ok, no unit test needed
    """
    Deletes file from filesystem when corresponding Attachment is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=Attachment)
def auto_delete_file_on_change(sender, instance, **kwargs):  # pragma: no cover
    # manual test was ok, no unit test needed
    """
    Deletes old file from filesystem when corresponding Attachment object is updated with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Attachment.objects.get(pk=instance.pk).file
    except Attachment.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
