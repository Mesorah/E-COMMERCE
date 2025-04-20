from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.functional_tests.base import BaseFunctionalTest
from utils.for_tests.base_for_setup import create_product_setup


class HomeIndexFunctionalTest(BaseFunctionalTest):
    def test_home_index_without_products_not_found_message(self):
        # User view the page
        self.browser.get(self.live_server_url)

        # See the body and realized that you don't have any product registered
        body = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn('Nenhum produto disponível', body.text)

    def test_home_index_hides_no_product_msg_with_products(self):
        create_product_setup()

        # User view the page
        self.browser.get(self.live_server_url)

        # See the body and realized that you have any product registered
        body = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertNotIn('Nenhum produto disponível', body.text)

    def test_home_index_serach_input_can_find_correct_product(self):
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

    def test_home_index_page_pagination(self):
        create_product_setup(11)

        # User view the page
        self.browser.get(self.live_server_url)

        # See the paginations pages
        pagination = self.browser.find_element(
            By.CLASS_NAME, 'current'
        ).text

        # See that there are 2 pages
        self.assertEqual(pagination, 'Page 1 of 2.')

        next_page = self.browser.find_element(
            By.XPATH,
            '//a[@href="?page=2"]'
        )

        # User click in the next page
        next_page.click()

        # See that have a product in the page 2
        product_title = self.browser.find_element(
            By.CLASS_NAME, 'product-name'
        ).text

        self.assertEqual(product_title, 'Product-0')
