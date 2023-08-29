import logging
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.messages import get_messages
from django.test.client import RequestFactory
from django.urls import reverse
from django.core import mail
from django.utils import translation
from .utils import create_one_time_login, one_time_login, send_one_time_login_mail


logger = logging.getLogger(__name__)


class OneTimeLoginModelTestCase(TestCase):
    """
    Tests all logic contained in the OneTimeLogin model.
    """

    def setUp(self):
        user = get_user_model().objects.create_user(
            "john",
            "lennon@thebeatles.com",
            "johnpassword")
        user.save()

    def test_get_absolute_url(self):
        user = get_user_model().objects.get(username='john')
        url = "/test/url"

        otl = create_one_time_login(user, url)

        abs_url = otl.get_absolute_url()

        logger.debug('test_get_absolute_url: url %s', abs_url)

        assert otl.secret in abs_url, 'secret is part of URL'


class UtilsTestCase(TestCase):
    """
    Tests all logic contained in the util functions.
    """

    def setUp(self):
        # prepare request factory
        self.factory = RequestFactory()

        # prepare test user
        user = get_user_model().objects.create_user(
            "john",
            "lennon@thebeatles.com",
            "johnpassword")
        user.save()

        # use english translations
        translation.activate('en')

    def test_create_one_time_login(self):
        user = get_user_model().objects.get(username='john')
        url = "/test/url"

        otl = create_one_time_login(user, url)

        assert len(otl.secret) > 10, 'length of secret'
        assert otl.user is user
        assert otl.url is url

    def test_one_time_login_ok(self):
        user = get_user_model().objects.get(username='john')
        url = "/test/url"

        otl = create_one_time_login(user, url)
        request = self.factory.get(otl.get_absolute_url())

        (otl_user, otl_url) = one_time_login(request, otl.secret)

        logger.debug('test_one_time_login_ok: user %s, url %s',
                     otl_user, otl_url)

        assert otl_user is not None, 'user was found'
        assert otl_user == user, 'user is the right one'
        assert otl_url == url, 'URL is the right one'

    def test_one_time_login_wrong(self):
        secret = "a_wrong_secret"

        url = reverse('one_time_login:login', args=[secret])

        request = self.factory.get(url)

        (otl_user, otl_url) = one_time_login(request, secret)

        logger.debug('test_one_time_login_wrong: user %s, url %s',
                     otl_user, otl_url)

        assert otl_user is None, 'user was not found'
        assert otl_url is None, 'no redirect URL'

    def test_one_time_login_used(self):
        user = get_user_model().objects.get(username='john')
        url = "/test/url"

        otl = create_one_time_login(user, url)
        request = self.factory.get(otl.get_absolute_url())
        # Add support django messaging framework
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        (otl_user, otl_url) = one_time_login(request, otl.secret)

        logger.debug('test_one_time_login_used: first try: user %s, url %s',
                     otl_user, otl_url)

        assert otl_user is not None, 'user was found'
        assert otl_user == user, 'user is the right one'
        assert otl_url == url, 'URL is the right one'

        (otl_user, otl_url) = one_time_login(request, otl.secret)

        logger.debug('test_one_time_login_used: second try: user %s, url %s',
                     otl_user, otl_url)

        assert otl_user is None, 'user was not found'
        assert otl_url is None, 'no redirect URL'

        messages = [m.message for m in get_messages(request)]

        logger.debug('test_one_time_login_used: messages %r', messages)

        assert len(messages) == 2, 'there are two message'
        assert 'used already' in str(messages[0]), 'already used message'
        assert 'new login link' in str(messages[1]), 'new login sent'

    def test_send_one_time_login_mail(self):
        user = get_user_model().objects.get(username='john')
        url = "/test/url"

        otl = create_one_time_login(user, url)
        request = self.factory.get(otl.get_absolute_url())
        # Add support django messaging framework
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))

        send_one_time_login_mail(otl.secret, user.email, request)

        messages = [m.message for m in get_messages(request)]

        logger.debug('test_send_one_time_login_mail: messages %r', messages)

        assert len(messages) == 1, 'there are two message'
        assert 'new login link' in str(messages[0]), 'new login sent'

        logger.debug('test_send_one_time_login_mail: outbox %r',
                     mail.outbox)

        sent_mail = mail.outbox[0]

        logger.debug('test_send_one_time_login_mail: to %r',
                     sent_mail.to)
        logger.debug('test_send_one_time_login_mail: content %r',
                     sent_mail.body)

        assert otl.user.email in sent_mail.to, 'receiver address'
        assert otl.get_absolute_url() in sent_mail.body, 'mail content'


class ViewsTestCase(TestCase):
    """
    Test one time login views.
    """

    def setUp(self):
        # prepare test user
        user = get_user_model().objects.create_user(
            "john",
            "lennon@thebeatles.com",
            "johnpassword")
        user.save()

        # use english translations
        translation.activate('en')

    def test_one_time_login_ok(self):
        user = get_user_model().objects.get(username='john')
        url = reverse('one_time_login:protected')

        otl = create_one_time_login(user, url)

        client = Client()

        response = client.get(otl.get_absolute_url())

        logger.debug('test_one_time_login: response %r', response)

        assert response.status_code == 302, 'response is redirect'
        assert response.url == reverse(
            'one_time_login:protected'), 'redirect URL'

    def test_one_time_login_wrong(self):
        client = Client()

        response = client.get(
            reverse('one_time_login:login', args=['1234567']))

        logger.debug('test_one_time_login: response %r', response)

        assert response.status_code == 302, 'response is redirect'
        assert response.url == '/', 'redirect URL'
