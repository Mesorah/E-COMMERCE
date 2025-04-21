from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.functional_tests.base import BaseFunctionalTest


class PaymentFunctionalTest(BaseFunctionalTest):
    def setUp(self):
        super().setUp()

        self.get_product_in_cart()

    def test_home_payment_works_if_all_data_is_correctly(self):
        # User view the page
        self.browser.get(self.live_server_url + reverse('home:payment'))

        # He saw that he was not logged in
        self.assertEqual(self.browser.title, 'Login')

        username = self.browser.find_element(By.ID, 'id_username')
        password = self.browser.find_element(By.ID, 'id_password')

        # Then logs into the site
        username.send_keys('Test')
        password.send_keys('Test')
        password.send_keys(Keys.ENTER)

        # He realized he was logged in and was redirected to Home
        self.assertEqual(self.browser.title, 'Home')

        self.fail('finish the test')
