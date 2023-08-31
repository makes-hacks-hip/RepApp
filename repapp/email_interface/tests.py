import logging
from django.test import TestCase
from django.conf import settings
from django.contrib.auth import get_user_model
from .forms import MessageForm
from .models import Message, Attachment


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


class MessageModelTestCase(TestCase):
    """
    Tests all logic contained in the Message model.
    """

    def setUp(self):
        john = get_user_model().objects.create_user(
            "john",
            "lennon@thebeatles.com",
            "johnpassword")
        john.save()
        self.john = john

        jane = get_user_model().objects.create_user(
            "jane",
            "doe@example.com",
            "janepassword")
        jane.save()
        self.jane = jane

        m1 = Message(
            summary='summary 1',
            html_content='<p>mail 1 HTML content</p>',
            text_content='mail 1 text content',
            sender=john,
            receiver=jane,
            sent=True,
            answered=True,
        )
        m1.save()
        self.m1 = m1

        m2 = Message(
            summary='summary 2',
            html_content='<p>mail 2 HTML content</p>',
            text_content='mail 2 text content',
            sender=jane,
            receiver=john,
            sent=True,
            answered=False,
            reply_to=m1,
        )
        m2.save()
        self.m2 = m2

        m3 = Message(
            summary='summary 3',
            html_content='<p>mail 3 HTML content</p>',
            text_content='mail 3 text content',
            sender=jane,
            receiver=john,
            sent=True,
            answered=False,
            reply_to=m1,
        )
        m3.save()
        self.m3 = m3

        a1 = Attachment(
            owner=john,
            name='johns_file.txt',
            mime_type='text/plain',
            file='uploads/johns_file.txt',
            message=m1,
        )
        a1.save()
        self.a1 = a1

        a2 = Attachment(
            owner=jane,
            name='janes_image.jpg',
            mime_type='image/jpeg',
            file='media/janes_image.jpg',
            message=m3,
        )
        a2.save()
        self.a2 = a2

        a3 = Attachment(
            owner=john,
            name='johns_image.jpg',
            mime_type='image/png',
            file='media/johns_image.jpg',
            message=m1,
        )
        a3.save()
        self.a3 = a3

    def test_str(self):
        assert self.m1.summary in str(self.m1)
        assert str(self.m1.receiver) in str(self.m1)

    def test_attachments(self):
        assert len(self.m1.attachments()) == 2
        assert self.m1.attachments()[0].pk == self.a1.pk
        assert self.m1.attachments()[1].pk == self.a3.pk
        assert len(self.m2.attachments()) == 0
        assert len(self.m3.attachments()) == 1
        assert self.m3.attachments()[0].pk == self.a2.pk

    def test_thread(self):
        assert len(self.m1.thread()) == 1
        assert self.m1.thread()[0].pk == self.m1.pk
        assert len(self.m2.thread()) == 2
        assert self.m2.thread()[0].pk == self.m1.pk
        assert self.m2.thread()[1].pk == self.m2.pk
        assert len(self.m3.thread()) == 2
        assert self.m3.thread()[0].pk == self.m1.pk
        assert self.m3.thread()[1].pk == self.m3.pk

    def test_answers(self):
        assert len(self.m1.answers()) == 2
        assert self.m1.answers()[0].pk == self.m2.pk
        assert self.m1.answers()[1].pk == self.m3.pk
        assert len(self.m2.answers()) == 0
        assert len(self.m3.answers()) == 0

    def test_siblings(self):
        assert len(self.m1.siblings()) == 0
        assert len(self.m2.siblings()) == 1
        assert self.m2.siblings()[0].pk == self.m3.pk
        assert len(self.m3.siblings()) == 1
        assert self.m3.siblings()[0].pk == self.m2.pk

    def test_to_user(self):
        assert len(Message.to_user(self.john)) == 2
        assert Message.to_user(self.john)[0].pk == self.m2.pk
        assert Message.to_user(self.john)[1].pk == self.m3.pk

        assert len(Message.to_user(self.jane)) == 1
        assert Message.to_user(self.jane)[0].pk == self.m1.pk

    def test_from_user(self):
        assert len(Message.from_user(self.john)) == 1
        assert Message.from_user(self.john)[0].pk == self.m1.pk

        assert len(Message.from_user(self.jane)) == 2
        assert Message.from_user(self.jane)[0].pk == self.m2.pk
        assert Message.from_user(self.jane)[1].pk == self.m3.pk


class AttachmentModelTestCase(TestCase):
    """
    Tests all logic contained in the Message model.
    """

    def setUp(self):
        john = get_user_model().objects.create_user(
            "john",
            "lennon@thebeatles.com",
            "johnpassword")
        john.save()
        self.john = john

        jane = get_user_model().objects.create_user(
            "jane",
            "doe@example.com",
            "janepassword")
        jane.save()
        self.jane = jane

        m1 = Message(
            summary='summary 1',
            html_content='<p>mail 1 HTML content</p>',
            text_content='mail 1 text content',
            sender=john,
            receiver=jane,
            sent=True,
            answered=True,
        )
        m1.save()
        self.m1 = m1

        m3 = Message(
            summary='summary 3',
            html_content='<p>mail 3 HTML content</p>',
            text_content='mail 3 text content',
            sender=jane,
            receiver=john,
            sent=True,
            answered=False,
            reply_to=m1,
        )
        m3.save()
        self.m3 = m3

        a1 = Attachment(
            owner=john,
            name='johns_file.txt',
            mime_type='text/plain',
            file='uploads/johns_file.txt',
            message=m1,
        )
        a1.save()
        self.a1 = a1

        a2 = Attachment(
            owner=jane,
            name='janes_image.jpg',
            mime_type='image/jpeg',
            file='media/janes_image.jpg',
            message=m3,
        )
        a2.save()
        self.a2 = a2

        a3 = Attachment(
            owner=john,
            name='johns_image.jpg',
            mime_type='image/png',
            file='media/johns_image.jpg',
            message=m1,
        )
        a3.save()
        self.a3 = a3

    def test_str(self):
        assert str(self.a1.file) in str(self.a1)
        assert str(self.m1) in str(self.a1)

    def test_get_absolute_url(self):
        assert settings.MEDIA_URL in self.a1.get_absolute_url()
        assert str(self.a1.file) in self.a1.get_absolute_url()

    def test_of_user(self):
        assert len(Attachment.of_user(self.john)) == 2
        assert Attachment.of_user(self.john)[0].pk == self.a1.pk
        assert Attachment.of_user(self.john)[1].pk == self.a3.pk

        assert len(Attachment.of_user(self.jane)) == 1
        assert Attachment.of_user(self.jane)[0].pk == self.a2.pk
