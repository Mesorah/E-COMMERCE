import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.browser import get_chrome_driver
from utils.for_tests.base_for_setup import create_product_setup


class StaffBaseFunctionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = get_chrome_driver()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=5):
        time.sleep(seconds)

    def login_user(
            self, reverse_url, username='test', password='123',
            return_super_user=False
    ):
        super_user = create_product_setup(return_super_user=return_super_user)

        self.browser.get(self.live_server_url + reverse('authors:login'))

        username_id = self.browser.find_element(By.ID, 'id_username')
        password_id = self.browser.find_element(By.ID, 'id_password')

        username_id.send_keys(username)
        password_id.send_keys(password)
        password_id.send_keys(Keys.ENTER)

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'products-container')
            )
        )

        self.browser.get(self.live_server_url + reverse(reverse_url))

        return super_user
