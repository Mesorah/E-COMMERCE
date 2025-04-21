import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from utils.browser import get_chrome_driver
from utils.for_tests.base_for_authentication import register_user
from utils.for_tests.base_for_setup import create_product_setup


class PaymentBaseFunctionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = get_chrome_driver()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=5):
        time.sleep(seconds)

    def get_product_in_cart(self):
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.ui import WebDriverWait

        register_user()
        product = create_product_setup()

        self.browser.get(self.live_server_url + reverse('authors:login'))

        username = self.browser.find_element(By.ID, 'id_username')
        password = self.browser.find_element(By.ID, 'id_password')

        username.send_keys('Test')
        password.send_keys('Test')
        password.send_keys(Keys.ENTER)

        wait = WebDriverWait(self.browser, 10)
        wait.until(
            EC.url_changes(self.live_server_url + reverse('authors:login'))
        )

        self.browser.get(self.live_server_url + reverse(
            'home:view_page', kwargs={'slug': product.name.lower()})
        )

        form = self.browser.find_element(By.CLASS_NAME, 'buy-form')
        form.submit()

        return form
