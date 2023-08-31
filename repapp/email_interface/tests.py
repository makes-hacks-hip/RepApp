import logging
from django.test import TestCase
from django.contrib.auth import get_user_model
from django import forms
from .forms import MessageForm


logger = logging.getLogger(__name__)


class MessageFormTestCase(TestCase):
    """
    Tests all logic contained in the OneTimeLogin model.
    """

    def setUp(self):
        user = get_user_model().objects.create_user(
            "john",
            "lennon@thebeatles.com",
            "johnpassword")
        user.save()

    def test_message_from_ok_no_text(self):
        user = get_user_model().objects.get(username='john')

        form = MessageForm({
            'receiver': user.pk,
            'summary': 'My mail summary',
            'html_content': '<p>Hallo, Welt!</p>',
            'mail_text': '',
            'use_mail_text': False,
        })

        assert form.is_valid(), 'form is valid'

        message = form.save(commit=False)

        logger.debug('Message: %s', message)
        logger.debug('Message text: %s', message.text_content)

        assert message.pk is None, 'message was not saved'
        assert message.receiver == user, 'receiver is set'
        assert message.sender is None, 'no sender is set'
        assert message.summary == 'My mail summary', 'summary is set'
        assert message.html_content == '<p>Hallo, Welt!</p>', 'HTML is set'
        assert 'Hallo, Welt!' in message.text_content, 'text was generated'

        message = form.save()

        assert message.pk is not None, 'message was saved'

    def test_message_from_ok_text(self):
        user = get_user_model().objects.get(username='john')

        form = MessageForm({
            'receiver': user.pk,
            'summary': 'My mail summary',
            'html_content': '<p>Hallo, Welt!</p>',
            'mail_text': 'Hallo!',
            'use_mail_text': True,
        })

        assert form.is_valid(), 'form is valid'

        message = form.save(commit=False)

        logger.debug('Message: %s', message)
        logger.debug('Message text: %s', message.text_content)

        assert message.pk is None, 'message was not saved'
        assert message.receiver == user, 'receiver is set'
        assert message.sender is None, 'no sender is set'
        assert message.summary == 'My mail summary', 'summary is set'
        assert message.html_content == '<p>Hallo, Welt!</p>', 'HTML is set'
        assert message.text_content == 'Hallo!', 'text was used'

    def test_message_from_wrong_no_text(self):
        user = get_user_model().objects.get(username='john')

        form = MessageForm({
            'receiver': user.pk,
            'summary': 'My mail summary',
            'html_content': '<p>Hallo, Welt!</p>',
            'mail_text': '',
            'use_mail_text': True,
        })

        logger.debug('Form data: text: %r', form)

        assert not form.is_valid()
        assert form.has_error('mail_text')
