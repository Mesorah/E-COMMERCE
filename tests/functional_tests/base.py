import time

# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By

from utils.browser import get_chrome_driver
from utils.for_tests.base_for_authentication import register_user
from utils.for_tests.base_for_setup import create_product_setup


class BaseFunctionalTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = get_chrome_driver()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=5):
        time.sleep(seconds)

    def get_product_in_cart(self):
        register_user()
        product = create_product_setup()

        self.browser.get(self.live_server_url + reverse(
            'home:view_page', kwargs={'slug': product.name.lower()})
        )

        form = self.browser.find_element(By.CLASS_NAME, 'buy-form')
        form.submit()

        return form
