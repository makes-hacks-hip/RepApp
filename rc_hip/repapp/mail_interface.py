import os
import re
import logging
from imap_tools import MailBox, AND, MailMessage
from django.core.mail import send_mail
from .models import Guest, Message, Question, Organisator

logger = logging.getLogger(__name__)


def send_message_notification(message: Message, guest: Guest):
    """
    Send new message notification.
    """
    organizers = []
    for organizer in Organisator.objects.all():
        organizers.append(organizer.mail)

    subject = f'Neue Nachricht von Gast {guest.name} ({guest.mail})'
    text = f'Hallo,\n'
    f'der Gast {guest.name} ({guest.mail}) hat folgende Nachricht gesendet:\n\n'
    f'{message.message}'
    # TODO: HTML message
    # TODO: add attachments
    # TODO: add link to message

    send_mail(
        subject=subject,
        message=text,
        from_email=os.getenv("DJANGO_SENDER_ADDRESS", ""),
        recipient_list=organizers,
        fail_silently=True
    )


def process_message(message: MailMessage, guest: Guest):
    """
    Process a valid message from a guest.
    """
    content = message.text
    if message.html:
        content = message.html

    result = re.search('Q#([0-9]+):', message.subject)
    if result:
        question_pk = result.group(1)
        question = Question.objects.filter(pk=question_pk).first()
        if question:
            if question.device.guest.mail == message.from_:
                question.answer = content
                question.save()
                # TODO: save attachments and add to message
                logger.info(
                    'Valid answer for Question %s from %s received.'
                    % (question_pk, message.from_))
                # TODO: send notifications
            else:
                logger.warning(
                    'Answer for Question %s from %s received,'
                    ' but the question was not for this guest. Message was ignored.'
                    % (question_pk, message.from_))
                # TODO: send reply that mail address was wrong
        else:
            logger.warning(
                'Answer for Question %s from %s received,'
                ' but there is no such question. Message was ignored.'
                % (question_pk, message.from_))
    else:
        db_message = Message(
            message=content,
            guest=guest,
        )
        db_message.save()
        send_message_notification(message, guest)


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
        guest = Guest.objects.filter(mail=sender).first()
        if guest:
            process_message(message, guest)
        else:
            logger.warning(
                'Mail form unknown sender %s with subject %s ignored.'
                % (sender, message.subject))

    return message_count
