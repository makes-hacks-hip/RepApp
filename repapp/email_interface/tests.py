import os
import logging
from pathlib import Path
from unittest.mock import patch
from django.test import TestCase, Client
from django.conf import settings
from django.test.client import RequestFactory
from django.contrib.auth import get_user_model
from django.core import mail
from django.utils import translation
from django.urls import reverse
from .forms import MessageForm
from .models import Message, Attachment
from .utils import create_message, send_message, process_message
from one_time_login.utils import create_one_time_login


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
    Tests all logic contained in the Attachment model.
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


class UtilsTestCase(TestCase):
    """
    Tests all logic contained in utils.
    """

    def setUp(self):
        # prepare request factory
        self.factory = RequestFactory()

        # prepare test data
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

        self.attachment_file = os.path.join(
            Path(__file__).resolve().parent, 'test_data', 'Nut.jpg')

    def test_create_message(self):
        request = self.factory.get('/')
        sent = create_message(
            request=request,
            sender=self.john,
            receiver=self.jane,
            summary='A test message',
            html_content='<p>Test HTML content</p>',
            text_content='Test text content',
            attachments=[self.attachment_file, '/does-not-exist'],
            reply_to=self.m1,
            send=False
        )

        assert not sent
        assert len(mail.outbox) == 0

        message = Message.objects.filter(summary='A test message').first()

        assert message.sender == self.john
        assert message.receiver == self.jane
        assert message.html_content == '<p>Test HTML content</p>'
        assert message.text_content == 'Test text content'
        assert message.reply_to == self.m1

        attachments = message.attachments()

        assert len(attachments) == 1
        assert 'Nut' in str(attachments[0].name)
        assert 'Nut' in str(attachments[0].file)
        assert 'image/jpeg' == attachments[0].mime_type
        assert attachments[0].owner == self.john
        assert attachments[0].message == message

        path = attachments[0].file.path

        logger.debug('Attachment file: %s', attachments[0].file.path)

        assert os.path.isfile(path)

        message.delete()
        # deleting the message should also delete the attachment and the file
        assert not os.path.isfile(path)

    def test_send_message(self):
        request = self.factory.get('/')

        create_message(
            request=request,
            sender=self.john,
            receiver=self.jane,
            summary='Another test message',
            html_content=f'<img src="{settings.MEDIA_URL}/image.jpg">',
            text_content='Test text content',
            attachments=[self.attachment_file, '/does-not-exist'],
            reply_to=self.m1,
            send=False
        )

        message = Message.objects.filter(
            summary='Another test message').first()

        sent = send_message(message=message, request=request)

        assert sent
        assert len(mail.outbox) == 1

        m = mail.outbox[0]

        assert len(m.recipients()) == 1
        assert self.jane.email in m.recipients()

        logger.debug('Mail sender: %r', m.from_email)

        assert m.from_email == settings.DEFAULT_FROM_EMAIL
        assert m.body == 'Test text content'

        logger.debug('Mail attachments: %r', len(m.attachments))

        assert 'Nut' in str(m.attachments[0])
        assert 'image/jpeg' in str(m.attachments[0])

        absolute_media_url = request.build_absolute_uri(settings.MEDIA_URL)

        assert absolute_media_url in m.message().as_string()

        message.delete()

    def test_create_message_and_send(self):
        request = self.factory.get('/')

        sent = create_message(
            request=request,
            sender=self.john,
            receiver=self.jane,
            summary='My test message',
            html_content='<p>Test HTML content</p>',
            text_content='Test text content',
            attachments=[self.attachment_file, '/does-not-exist'],
            reply_to=self.m1,
            send=True
        )

        assert sent
        assert len(mail.outbox) == 1

        message = Message.objects.filter(summary='My test message').first()

        message.delete()

    def test_process_message_no_guest(self):
        with patch('imap_tools.MailMessage') as MockClass:
            mock = MockClass.return_value

            mock.from_ = 'noguest@example.com'
            mock.subject = 'subject'

            processed = process_message(mock)

            assert not processed

    def test_process_message_reply(self):
        with patch('imap_tools.MailMessage') as MockClass:
            mock = MockClass.return_value

            mock.from_ = self.m1.receiver.email
            mock.subject = f'Re: {self.m1.summary}'
            mock.html = '<p>HTML content</p>'
            mock.text = 'Text content'
            mock.attachments = []

            processed = process_message(mock)

            assert processed
            assert self.m1.answered

            message = Message.objects.filter(summary=mock.subject).first()

            assert message.reply_to == self.m1

            assert message.sender == self.m1.receiver
            assert message.receiver == self.m1.sender
            assert message.summary == f'Re: {self.m1.summary}'
            assert message.html_content == '<p>HTML content</p>'
            assert message.text_content == 'Text content'

    def test_process_message_new_message(self):
        with patch('imap_tools.MailMessage') as MockClass:
            mock = MockClass.return_value

            mock.from_ = self.m1.receiver.email
            mock.subject = 'New message'
            mock.html = '<p>HTML content</p>'
            mock.text = 'Text content'
            mock.attachments = []

            processed = process_message(mock)

            assert processed

            message = Message.objects.filter(summary=mock.subject).first()

            assert message.reply_to == None
            assert message.sender == self.m1.receiver
            assert message.receiver == None
            assert message.summary == 'New message'
            assert message.html_content == '<p>HTML content</p>'
            assert message.text_content == 'Text content'

    def test_process_message_attachments(self):
        with patch('imap_tools.MailMessage') as MockClass:
            with patch('imap_tools.MailAttachment') as MockAttachmentClass:
                with open(self.attachment_file, "rb") as file:
                    mock = MockClass.return_value
                    attachment_mock = MockAttachmentClass.return_value

                    attachment_mock.filename = 'test.jpg'
                    attachment_mock.content_type = 'image/jpeg'
                    attachment_mock.payload = file.read()

                    mock.from_ = self.m1.receiver.email
                    mock.subject = 'New message with attachment'
                    mock.html = '<p>HTML content</p>'
                    mock.text = 'Text content'
                    mock.attachments = [attachment_mock]

                    processed = process_message(mock)

                    assert processed

                    message = Message.objects.filter(
                        summary=mock.subject).first()

                    assert message.reply_to == None
                    assert message.sender == self.m1.receiver
                    assert message.receiver == None
                    assert message.summary == 'New message with attachment'
                    assert message.html_content == '<p>HTML content</p>'
                    assert message.text_content == 'Text content'

                    attachment = Attachment.objects.filter(
                        message=message).first()

                    logger.debug('Attachment: %r', attachment)

                    assert attachment.owner == self.m1.receiver
                    assert 'test' in attachment.name
                    assert attachment.mime_type == 'image/jpeg'
                    assert 'test' in attachment.file.path
                    assert os.path.isfile(attachment.file.path)

                    message.delete()
                    # deleting the message should also delete the attachment and the file
                    assert not os.path.isfile(attachment.file.path)


class ViewsTestCase(TestCase):
    """
    Test email interface views.
    """

    def setUp(self):
        # use english translations
        translation.activate('en')

        # prepare test data
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

    def test_my_attachments_is_protected(self):
        url = reverse('email_interface:my_attachments')

        client = Client()

        response = client.get(url, follow=True)
        logger.debug('test_my_attachments_is_protected: %r',
                     response.redirect_chain[-1])

        last_url, status_code = response.redirect_chain[-1]
        assert status_code == 302
        assert last_url == '/accounts/login/?next=/en/emails/attachments/'

    def test_my_attachments(self):
        user = get_user_model().objects.get(username='john')

        url = reverse('email_interface:my_attachments')
        otl = create_one_time_login(user, url)

        client = Client()

        response = client.get(otl.get_absolute_url(), follow=True)

        assert response.status_code == 200, 'response is OK'
        last_url, _ = response.redirect_chain[-1]
        assert last_url == url, 'redirect URL'

        self.assertContains(response, 'johns_file.txt')
        self.assertContains(response, 'johns_image.jpg')
        self.assertNotContains(response, 'janes_image')

    def test_my_received_mails_is_protected(self):
        url = reverse('email_interface:my_received_mails')

        client = Client()

        response = client.get(url, follow=True)
        logger.debug('test_my_received_mails_is_protected: %r',
                     response.redirect_chain[-1])

        last_url, status_code = response.redirect_chain[-1]
        assert status_code == 302
        assert last_url == '/accounts/login/?next=/en/emails/received/'

    def test_my_received_mails(self):
        user = get_user_model().objects.get(username='john')

        url = reverse('email_interface:my_received_mails')
        otl = create_one_time_login(user, url)

        client = Client()

        response = client.get(otl.get_absolute_url(), follow=True)

        assert response.status_code == 200, 'response is OK'
        last_url, _ = response.redirect_chain[-1]
        assert last_url == url, 'redirect URL'

        self.assertContains(response, '<p>mail 3 HTML content</p>')
        self.assertContains(response, 'janes_image')
        self.assertNotContains(response, '<p>mail 1 HTML content</p>')

    def test_my_sent_mails_is_protected(self):
        url = reverse('email_interface:my_sent_mails')

        client = Client()

        response = client.get(url, follow=True)
        logger.debug('test_my_sent_mails_is_protected: %r',
                     response.redirect_chain[-1])

        last_url, status_code = response.redirect_chain[-1]
        assert status_code == 302
        assert last_url == '/accounts/login/?next=/en/emails/sent/'

    def test_my_sent_mails(self):
        user = get_user_model().objects.get(username='john')

        url = reverse('email_interface:my_sent_mails')
        otl = create_one_time_login(user, url)

        client = Client()

        response = client.get(otl.get_absolute_url(), follow=True)

        assert response.status_code == 200, 'response is OK'
        last_url, _ = response.redirect_chain[-1]
        assert last_url == url, 'redirect URL'

        self.assertContains(response, '<p>mail 1 HTML content</p>')
        self.assertNotContains(response, '<p>mail 3 HTML content</p>')

    def test_mail_thread_is_protected(self):
        url = reverse('email_interface:mail_thread', kwargs={'id': self.m3.pk})

        client = Client()

        response = client.get(url, follow=True)
        logger.debug('test_my_received_mails_is_protected: %r',
                     response.redirect_chain[-1])

        last_url, status_code = response.redirect_chain[-1]
        assert status_code == 302
        assert last_url == f'/accounts/login/?next=/en/emails/{self.m3.pk}/view/'

    def test_mail_thread(self):
        user = get_user_model().objects.get(username='john')

        url = reverse('email_interface:mail_thread', kwargs={'id': self.m3.pk})
        otl = create_one_time_login(user, url)

        client = Client()

        response = client.get(otl.get_absolute_url(), follow=True)

        assert response.status_code == 200, 'response is OK'
        last_url, _ = response.redirect_chain[-1]
        assert last_url == url, 'redirect URL'

        self.assertContains(response, '<p>mail 3 HTML content</p>')
        self.assertContains(response, 'janes_image')
        self.assertContains(response, '<p>mail 1 HTML content</p>')

    def test_mail_thread_reply(self):
        user = get_user_model().objects.get(username='john')

        url = reverse('email_interface:mail_thread', kwargs={'id': self.m3.pk})
        otl = create_one_time_login(user, url)

        client = Client()

        response = client.get(otl.get_absolute_url(), follow=True)

        assert response.status_code == 200, 'response is OK'
        last_url, _ = response.redirect_chain[-1]
        assert last_url == url, 'redirect URL'

        response = client.post(url, {
            'html_content': '<p>The reply content.</p>',
            'receiver': self.jane.pk,
            'use_mail_text': '',
            'mail_text': '',
        }, follow=True)

        logger.debug('Post response: %r', response)

        message = Message.objects.filter(reply_to=self.m3).first()

        url = reverse('email_interface:mail_thread', kwargs={'id': message.pk})

        assert response.status_code == 200, 'response is OK'
        last_url, _ = response.redirect_chain[-1]
        assert last_url == url, 'redirect URL'

        self.assertContains(response, 'Mail was sent.')

        assert len(mail.outbox) == 1

        logger.debug('Outbox: %r', mail.outbox[0].subject)

        assert mail.outbox[0].subject == 'Re: summary 3'
        assert self.jane.email in mail.outbox[0].recipients()

        assert message.reply_to == self.m3
        assert message.sender == user
        assert message.receiver == self.jane
        assert message.summary == 'Re: summary 3'
        assert message.html_content == '<p>The reply content.</p>'
        assert 'The reply content.' in message.text_content
