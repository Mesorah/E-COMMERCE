from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.functional_tests.staff.base import StaffBaseFunctionalTest
from utils.for_tests.base_for_setup import create_ordered_setup


class ClientsListsFunctionalTest(StaffBaseFunctionalTest):
    def setUp(self):
        super().setUp()

        self.super_user = self.login_user(
            reverse_url='staff:clients', return_super_user=True
        )

        self.browser.get(self.live_server_url + reverse('staff:clients'))

    def test_clients_lists_hide_a_correct_user(self):
        # Find a username
        order_text = self.browser.find_element(
            By.CLASS_NAME, 'order-text'
        ).text

        self.assertEqual('Nome: test', order_text)

    def test_clients_lists_user_get_a_empty_orders_message(self):
        # Find and click the "View" button
        visualization_button = self.browser.find_element(
            By.XPATH, "//a[text()='Visualizar']"
        )

        visualization_button.click()

        # Wait until the "Orders" title appears on the page
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h1[text()='Pedidos']")
            )
        )

        # Check if the empty page message appears when there are no orders
        empty_base_page = self.browser.find_element(
            By.CLASS_NAME, 'empty-base-page'
        ).text

        self.assertEqual('Nenhum pedido feito.', empty_base_page)

    def test_clients_lists_user_get_orders(self):
        create_ordered_setup(self.super_user)

        # Find and click the "View" button
        visualization_button = self.browser.find_element(
            By.XPATH, "//a[text()='Visualizar']"
        )

        visualization_button.click()

        # Wait until the "Orders" title appears on the page
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h1[text()='Pedidos']")
            )
        )

        # Find the ordered product name on the page
        ordered_name = self.browser.find_element(
            By.CLASS_NAME, 'order-text'
        ).text

        self.assertEqual('Nome: Test-1', ordered_name)

    def test_clients_lists_search_input_can_find_correct_client(self):
        # See a search field with the text "Search for a client"
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a client"]'
        )

        # Search for the name "test"
        # to find a client with that username
        search_input.send_keys('test')
        search_input.send_keys(Keys.ENTER)

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'order-text')
            )
        )

        client_username = self.browser.find_element(
            By.CLASS_NAME, 'order-text'
        ).text

        # The user sees what they were looking for on the page
        self.assertEqual(client_username, 'Nome: test')
