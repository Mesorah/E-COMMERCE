from selenium.webdriver.common.by import By

from tests.functional_tests.base import BaseFunctionalTest
from utils.for_tests.base_for_setup import create_product_setup


class HomeIndexFunctionalTest(BaseFunctionalTest):
    def test_home_index_without_products_not_found_message(self):
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Nenhum produto disponível', body.text)

    def test_no_product_message_is_not_displayed_when_products_exist(self):
        create_product_setup()
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertNotIn('Nenhum produto disponível', body.text)
