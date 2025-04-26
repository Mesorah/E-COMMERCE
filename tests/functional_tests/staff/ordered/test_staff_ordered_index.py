from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.functional_tests.staff.base import StaffBaseFunctionalTest
from utils.for_tests.base_for_setup import create_ordered_setup


class StaffOrderedIndexFunctionalTest(StaffBaseFunctionalTest):
    def setUp(self):
        super().setUp()

        self.super_user = self.login_user(
            reverse_url='staff:ordered_index', return_super_user=True
        )

        self.browser.get(self.live_server_url + reverse('staff:ordered_index'))

    def test_staff_ordered_index_without_products_not_found_message(self):
        # See the empty page and realized that you don't
        # have any ordered registered
        empyty_page = self.browser.find_element(
            By.CLASS_NAME, 'empty-base-page'
        ).text

        self.assertIn('Nenhum pedido feito.', empyty_page)

    def test_staff_ordered_index_hides_no_product_msg_with_products(self):
        create_ordered_setup(self.super_user)
        self.browser.refresh()

        # See the empty page and realized that you
        # have any ordered registered
        body = self.browser.find_element(
            By.TAG_NAME, 'body'
        ).text

        self.assertNotIn('Nenhum pedido feito.', body)

    def test_staff_ordered_index_search_input_can_find_correct_product(self):
        create_ordered_setup()
        self.browser.refresh()

        # See a search field with the text "Search for a ordered"
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a ordered"]'
        )

        # Search for the name "Test First"
        # to find a ordered with that username
        search_input.send_keys('Test-1')
        search_input.send_keys(Keys.ENTER)

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'order-title')
            )
        )

        ordered_name = self.browser.find_element(
            By.XPATH, "//p[contains(text(), 'Test-')]"
        ).text

        # The user sees what they were looking for on the page
        self.assertIn('Nome: Test-', ordered_name)

    def test_staff_ordered_index_page_pagination(self):
        create_ordered_setup(qtd=11)
        self.browser.refresh()

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

        # See that have a ordered in the page 2
        ordered_name = self.browser.find_element(
            By.XPATH, "//p[contains(text(), 'Test-11')]"
        ).text

        self.assertEqual(ordered_name, 'Nome: Test-11')
