from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.functional_tests.base import BaseFunctionalTest
from utils.for_tests.base_for_setup import create_product_setup


class HomeSearchFunctionalTest(BaseFunctionalTest):
    def test_home_search_serach_input_can_find_correct_product(self):
        create_product_setup(10)

        # User view the page
        self.browser.get(self.live_server_url)

        # See a search field with the text "Search for a product"
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a product"]'
        )

        # Search for the name "Product-1" to find a product with that title
        search_input.send_keys('Product-1')
        search_input.send_keys(Keys.ENTER)

        product_title = self.browser.find_element(
            By.CLASS_NAME, 'product-name'
        ).text

        # The user sees what they were looking for on the page
        self.assertEqual(product_title, 'Product-1')
