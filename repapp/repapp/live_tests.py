import time
import logging
from django.contrib.auth import get_user_model
from django.utils import translation
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from one_time_login.utils import create_one_time_login
from email_interface.models import Message, Attachment


logger = logging.getLogger(__name__)


class LiveOneTimeLoginTests(StaticLiveServerTestCase):
    """
    Live server test for one time login
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(50)
        cls.selenium.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        super().setUp()

        # prepare test user
        user = get_user_model().objects.create_user(
            "john",
            "lennon@thebeatles.com",
            "johnpassword")
        user.save()

        # use english translations
        translation.activate('en')

        # prepare one time login
        user = get_user_model().objects.get(username='john')
        self.url = reverse('one_time_login:protected')
        otl = create_one_time_login(user, self.url)
        self.otl_url = otl.get_absolute_url()

    def test_one_time_login(self):
        url = f"{self.live_server_url}{self.otl_url}"
        logger.debug('Opening one time login URL %s', url)
        self.selenium.get(url)

        time.sleep(2)

        self.assertTrue('protected content' in self.selenium.page_source)
        self.assertTrue(self.url in self.selenium.current_url)


class LiveEmailInterfaceTests(StaticLiveServerTestCase):
    """
    Live server test for email interface
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(50)
        cls.selenium.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        super().setUp()

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

        # use english translations
        translation.activate('en')

    def test_sent(self):
        url = reverse('email_interface:my_sent_mails')
        otl = create_one_time_login(self.john, url)
        url = f"{self.live_server_url}{otl.get_absolute_url()}"

        self.selenium.get(url)

        time.sleep(2)

        self.assertTrue(
            "<p>mail 1 HTML content</p>" in self.selenium.page_source)

    def test_received(self):
        url = reverse('email_interface:my_received_mails')
        otl = create_one_time_login(self.john, url)
        url = f"{self.live_server_url}{otl.get_absolute_url()}"

        self.selenium.get(url)

        time.sleep(2)

        self.assertTrue(
            "<p>mail 3 HTML content</p>" in self.selenium.page_source)
        self.assertTrue(
            "<p>mail 2 HTML content</p>" in self.selenium.page_source)
        self.assertTrue("janes_image.jpg" in self.selenium.page_source)

    def test_attachments(self):
        url = reverse('email_interface:my_attachments')
        otl = create_one_time_login(self.john, url)
        url = f"{self.live_server_url}{otl.get_absolute_url()}"

        self.selenium.get(url)

        time.sleep(2)

        self.assertTrue("johns_file.txt" in self.selenium.page_source)
        self.assertTrue("johns_image.jpg" in self.selenium.page_source)

    def test_view(self):
        url = reverse('email_interface:mail_thread', kwargs={'id': self.m3.pk})
        otl = create_one_time_login(self.john, url)
        url = f"{self.live_server_url}{otl.get_absolute_url()}"

        self.selenium.get(url)

        time.sleep(2)

        self.assertTrue(
            "<p>mail 3 HTML content</p>" in self.selenium.page_source)
        self.assertTrue(
            "<p>mail 1 HTML content</p>" in self.selenium.page_source)
        self.assertTrue("janes_image.jpg" in self.selenium.page_source)
        self.assertTrue("summary 2" in self.selenium.page_source)
        self.assertTrue(
            "<p>mail 2 HTML content</p>" not in self.selenium.page_source)
