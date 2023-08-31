import time
import logging
from django.contrib.auth import get_user_model
from django.utils import translation
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from one_time_login.utils import create_one_time_login


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

        # prepare test user
        user = get_user_model().objects.create_user(
            "john",
            "lennon@thebeatles.com",
            "johnpassword")
        user.save()

        # use english translations
        translation.activate('en')

    def test_process(self):
        pass

    def test_sent(self):
        pass

    def test_received(self):
        pass

    def test_attachments(self):
        pass

    def test_view(self):
        pass

    def test_test_mail(self):
        pass

    def test_send_mail(self):
        pass
