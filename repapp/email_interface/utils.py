import os
import mimetypes
import logging
from imap_tools import MailBox, AND, MailMessage
from django.core.files.base import ContentFile
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Message, Attachment
from .signals import message_answered, new_message


logger = logging.getLogger(__name__)


def create_message(request, sender, receiver, summary, html_content, text_content, attachments=[], reply_to=None, send=True) -> bool:
    """
    Create a new email message, and send it if send is True.
    """
    message = Message(
        sender=sender,
        receiver=receiver,
        summary=summary,
        html_content=html_content,
        text_content=text_content,
        reply_to=reply_to
    )
    message.save()

    logger.debug('New message %s', message)

    for attachment in attachments:
        if not os.path.isfile(attachment):
            logger.debug('Attachment not found: %s', attachment)
            continue

        _, name = os.path.split(attachment)
        mime_type = mimetypes.guess_type(attachment)

        if not attachment.startswith(settings.MEDIA_ROOT):
            with open(attachment, "rb") as file:
                # copy file
                attachment = ContentFile(file.read(), name)

        a = Attachment(
            owner=sender,
            name=name,
            mime_type=mime_type,
            file=attachment,
            message=message
        )
        a.save()

        logger.debug('New attachment %s', a)

    message.save()

    if send:
        return send_message(message, request)

    return False


def send_message(message, request):
    """
    Send a message as email.
    """
    # make media urls absolute
    absolute_media_url = request.build_absolute_uri(settings.MEDIA_URL)

    logger.debug('Media URL: %s, absolute media url: %s',
                 settings.MEDIA_URL, absolute_media_url)

    html_content = message.html_content
    html_content = html_content.replace(settings.MEDIA_URL, absolute_media_url)

    # Create email message
    email = EmailMultiAlternatives(message.summary, message.text_content,
                                   settings.DEFAULT_FROM_EMAIL, [message.receiver.email])
    email.attach_alternative(html_content, "text/html")

    for attachment in Attachment.objects.filter(message=message):
        with open(attachment.file.path, 'rb') as file:
            file_content = file.read()
            email.attach(attachment.name, file_content, attachment.mime_type)

    try:
        res = email.send()
    except:
        # Sending mail cause an exception
        return False

    if res > 0:
        message.sent = True
        message.save()
        return True

    return False


def process_message(mail_message: MailMessage, guest):
    """
    Process a valid message from a guest.
    """
    receiver = None
    reply_to = None

    if mail_message.subject.startswith('Re:'):
        summary = mail_message.subject.replace('Re:', '').strip()
        reply_to = Message.objects.filter(
            receiver=guest, summary__icontains=summary).first()

        if reply_to:
            receiver = reply_to.sender
            reply_to.answered = True
            reply_to.save()

            logger.debug('Answer received for %s', reply_to)

    html_content = None
    if mail_message.html:
        html_content = mail_message.html

    message = Message(
        sender=guest,
        receiver=receiver,
        summary=mail_message.subject,
        html_content=html_content,
        text_content=mail_message.text,
        reply_to=reply_to,
    )
    message.save()

    if reply_to:
        # trigger message answered signal
        message_answered.send(
            sender=Message, instance=reply_to, answer=message)
    else:
        # trigger new message signal
        new_message.send(sender=Message, instance=message)

    logger.debug('Received message %s', message)

    for attachment in mail_message.attachments:
        name = attachment.filename
        mime_type = attachment.content_type
        file = ContentFile(attachment.payload, name)

        logger.debug('Processing attachment %s (%s) of message %s',
                     name, mime_type, message)

        a = Attachment(
            owner=guest,
            name=name,
            mime_type=mime_type,
            file=file,
            message=message
        )
        a.save()

        logger.debug('New attachment %s', a)


def process_mails():
    """
    Check for new messages and handle valid messages.
    """
    host = os.getenv("DJANGO_EMAIL_HOST", "")
    user = os.getenv("DJANGO_EMAIL_HOST_USER", None)
    password = os.getenv("DJANGO_EMAIL_HOST_PASSWORD", None)
    mailbox = MailBox(host).login(user, password)
    messages = mailbox.fetch(criteria=AND(seen=False),
                             mark_seen=True, bulk=True)

    message_count = 0
    for message in messages:
        message_count += 1
        sender = message.from_

        guest = get_user_model().objects.filter(email=sender, is_active=True).first()
        if guest:
            process_message(message, guest)
        else:
            logger.info(
                'Mail form unknown sender %s with subject %s ignored.', sender, message.subject)

    logger.debug('Processed %d new messages', message_count)

    return message_count
