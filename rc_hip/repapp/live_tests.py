import time
import os
import datetime
import random
from pathlib import Path
from hashlib import sha256
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.firefox.webdriver import WebDriver
from .models import CustomUser, Guest, OneTimeLogin


class WorkflowTests(StaticLiveServerTestCase):
    """
    Tests for workflows.
    """
    fixtures = ["cafe-data.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        super().setUp()

        self.password = "ATestPassword"
        user = CustomUser.objects.get(pk=3)
        user.set_password(self.password)
        user.save()
        self.user = user
        print(f'Password of user {user.email} updated to {self.password}.')

        url = "/guest/profile/"
        secret = sha256(
            f'{user.email}{url}{datetime.datetime.now()}{random.randint(0,9999999)}'.encode(
                'utf-8')
        ).hexdigest()
        self.secret = secret
        secret_hash = sha256(secret.encode('utf-8')).hexdigest()
        one_time_login = OneTimeLogin(
            secret=secret_hash,
            user=user,
            url=url,
        )
        one_time_login.save()
        self.one_time_login = one_time_login

    def test_register_device(self):
        """
        Test device registration flows.
        """
        # Open landing page
        self.selenium.get(f"{self.live_server_url}/")
        # Click on a register link
        self.selenium.find_element(By.CLASS_NAME, "register_link").click()
        time.sleep(1)
        # Enter new device
        # Enter guest mail address
        mail = self.selenium.find_element(By.NAME, "mail")
        mail.send_keys("guest@example.com")
        # Enter device
        device = self.selenium.find_element(By.NAME, "device")
        device.send_keys("A Test Device")
        # Enter manufacturer
        manufacturer = self.selenium.find_element(By.NAME, "manufacturer")
        manufacturer.send_keys("A Test Manufacturer")
        # Enter a error description
        error = self.selenium.find_element(By.NAME, "error")
        error.send_keys("A description of the issue\nof the device.")
        # Skip device picture and device type plate
        # No follow up repair
        # Accept repair conditions
        self.selenium.find_element(By.NAME, "confirm_repair").click()
        # Accept data protection notice
        self.selenium.find_element(By.NAME, "confirm_data").click()
        time.sleep(1)
        # Send form
        self.selenium.find_element(By.CLASS_NAME, 'submit_button').click()
        time.sleep(1)
        # Register new guest
        # Enter guest name
        name = self.selenium.find_element(By.NAME, "name")
        name.send_keys("A Guest")
        # Enter guest phone
        phone = self.selenium.find_element(By.NAME, "phone")
        phone.send_keys("0911 123 456")
        # Enter guest residence
        residence = self.selenium.find_element(By.NAME, "residence")
        residence.send_keys("Musterstadt")
        time.sleep(1)
        # Send form
        self.selenium.find_element(By.CLASS_NAME, 'submit_button').click()
        time.sleep(1)
        self.assertTrue("confirm" in self.selenium.current_url)
        self.assertTrue("Anmeldung erfolgreich!" in self.selenium.page_source)
        # Register second device
        # Open landing page again
        self.selenium.get(f"{self.live_server_url}/")
        # Click on a register link
        self.selenium.find_element(By.CLASS_NAME, "register_link").click()
        time.sleep(1)
        # Enter new device
        # Enter guest mail address
        mail = self.selenium.find_element(By.NAME, "mail")
        mail.send_keys("guest@example.com")
        # Enter device
        device = self.selenium.find_element(By.NAME, "device")
        device.send_keys("Another Test Device")
        # Enter manufacturer
        manufacturer = self.selenium.find_element(By.NAME, "manufacturer")
        manufacturer.send_keys("Another Test Manufacturer")
        # Enter a error description
        error = self.selenium.find_element(By.NAME, "error")
        error.send_keys("Another issue description.")
        # Add device picture
        test_script_folder = Path(__file__).resolve().parent
        fixtures_folder = os.path.join(test_script_folder, "fixtures")
        device_picture_file = os.path.join(fixtures_folder, "Hummingbird.jpg")
        device_picture = self.selenium.find_element(By.NAME, "device_picture")
        device_picture.send_keys(device_picture_file)
        print(f"Using device picture {device_picture_file}")
        # Add type plate picture
        type_plate_picture_file = os.path.join(fixtures_folder, "Nut.jpg")
        type_plate_picture = self.selenium.find_element(
            By.NAME, "type_plate_picture")
        type_plate_picture.send_keys(type_plate_picture_file)
        print(f"Using type plate picture {type_plate_picture_file}")
        # Select as follow up repair
        self.selenium.find_element(By.NAME, "follow_up").click()
        # Accept repair conditions
        self.selenium.find_element(By.NAME, "confirm_repair").click()
        # Accept data protection notice
        self.selenium.find_element(By.NAME, "confirm_data").click()
        time.sleep(1)
        # Send form
        self.selenium.find_element(By.CLASS_NAME, 'submit_button').click()
        time.sleep(1)
        # Guest is known, no guest registration needed.
        self.assertTrue("confirm" in self.selenium.current_url)
        self.assertTrue("Anmeldung erfolgreich!" in self.selenium.page_source)

    def test_login_and_view_profile(self):
        """
        Test login and profile page.
        """
        # Open login form
        self.selenium.get(f"{self.live_server_url}/accounts/login/")
        # Enter login data
        # Enter guest mail address
        username = self.selenium.find_element(By.NAME, "username")
        username.send_keys(self.user.email)
        # Enter password
        password = self.selenium.find_element(By.NAME, "password")
        password.send_keys(self.password)
        time.sleep(1)
        # Submit form
        self.selenium.find_element(
            By.XPATH, '//button[@type="submit"]').click()
        time.sleep(1)
        self.selenium.get(f"{self.live_server_url}/guest/profile/")
        time.sleep(1)
        self.assertTrue(self.user.email in self.selenium.page_source)
        self.assertTrue("/guest/profile/" in self.selenium.current_url)
        time.sleep(1)

    def test_one_time_login_and_view_device(self):
        """
        Test one time login and device page.
        """
        # Open login form
        self.selenium.get(
            f"{self.live_server_url}/onetimelogin/{self.secret}/")
        time.sleep(1)
        self.assertTrue(self.user.email in self.selenium.page_source)
        self.assertTrue("Login erfolgreich" in self.selenium.page_source)
        self.assertTrue("/guest/profile/" in self.selenium.current_url)
        time.sleep(1)
        self.selenium.get(
            f"{self.live_server_url}/device/5f3d413409ca9c90c99540fd5677cc1147156f100d7bd29d3a1c1940e5f2c6ac/")
        time.sleep(1)
        self.assertTrue("Test Gerät" in self.selenium.page_source)
        self.assertTrue("Test Hersteller" in self.selenium.page_source)
        self.assertTrue("/device/" in self.selenium.current_url)
        time.sleep(1)

    def test_member_login(self):
        self.selenium.get(
            f"{self.live_server_url}/member/login/")
        time.sleep(1)
        self.selenium.find_element(By.CLASS_NAME, 'login_link').click()
        time.sleep(1)
        self.assertTrue('sso.makes-hacks-hip.de' in self.selenium.current_url)
