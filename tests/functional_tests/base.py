import time

# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from utils.browser import get_chrome_driver
from utils.for_tests.base_for_authentication import (  # noqa E501
    register_super_user,
    register_user,
)
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

    def login_user(
            self, username='Test', password='Test',
            normal_user=True, super_user=False,
            create_product=True
    ):
        if normal_user:
            register_user()

        if super_user:
            super_user_profile = register_super_user()

        if create_product:
            if super_user:
                product = create_product_setup(
                    super_user_profile=super_user_profile
                )

            else:
                product = create_product_setup()

        self.browser.get(self.live_server_url + reverse('authors:login'))

        username_id = self.browser.find_element(By.ID, 'id_username')
        password_id = self.browser.find_element(By.ID, 'id_password')

        username_id.send_keys(username)
        password_id.send_keys(password)
        password_id.send_keys(Keys.ENTER)

        if create_product:
            return product

        return

    def get_product_in_cart(self, username='Test', password='Test'):
        product = self.login_user(username, password)

        self.browser.get(self.live_server_url + reverse(
            'home:view_page', kwargs={'slug': product.name.lower()})
        )

        form = self.browser.find_element(By.CLASS_NAME, 'buy-form')
        form.submit()

        return form
