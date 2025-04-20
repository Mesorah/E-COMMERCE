from django.urls import reverse
from selenium.webdriver.common.by import By

from tests.functional_tests.authors.base import AuthorsBaseFunctionalTest
from utils.for_tests.base_for_authentication import register_user


class AuthorsLoginFunctionalTest(AuthorsBaseFunctionalTest):
    def setUp(self):
        super().setUp()
        self.browser.get(self.live_server_url + reverse('authors:login'))
        self.user = register_user()

    def test_authors_login_user_valid_data_can_long_successfully(self):
        username = self.browser.find_element(By.ID, 'id_username')
        password = self.browser.find_element(By.ID, 'id_password')

        # User enters his username and password
        username.send_keys('Test')
        password.send_keys('Test')

        form = self.browser.find_element(By.TAG_NAME, 'form')
        form.submit()

        # User notices through the title that he entered the home page
        self.assertEqual(self.browser.title, 'Home')
