import time
import os
from pathlib import Path
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver


class WorkflowTests(StaticLiveServerTestCase):
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

    def test_register_device(self):
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
