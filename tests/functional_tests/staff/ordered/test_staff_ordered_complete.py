from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.functional_tests.staff.base import StaffBaseFunctionalTest
from utils.for_tests.base_for_setup import create_ordered_setup


class StaffOrderedCompleteFunctionalTest(StaffBaseFunctionalTest):
    def setUp(self):
        super().setUp()

        self.super_user = self.login_user(
            reverse_url='staff:ordered_index', return_super_user=True
        )

    def test_staff_ordered_complete_shows_not_found_without_orders(self):
        self.browser.get(self.live_server_url + reverse(
            'staff:ordered_complete'
        ))

        # See the empty page and realized that you don't
        # have any ordered completed
        empyty_page = self.browser.find_element(
            By.CLASS_NAME, 'empty-base-page'
        ).text

        self.assertIn('Nenhum pedido completo.', empyty_page)

    def test_staff_ordered_complete_hides_a_correct_products(self):
        create_ordered_setup(self.super_user)
        self.browser.refresh()

        # Find and click the "View" button
        button = self.browser.find_element(
            By.XPATH, "//a[text()='Visualizar']"
        )

        button.click()

        # Wait until the order title appears on the page
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'order-title')
            )
        )

        # Find and click the "Complete Order" button
        complete_button = self.browser.find_element(
            By.XPATH, "//button[text()='Concluir Pedido']"
        )

        complete_button.click()

        # Accept the alert popup
        alert = self.browser.switch_to.alert
        alert.accept()

        # Wait until the order empty message appears on the page
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'empty-base-page')
            )
        )

        # Check if the empty page message appears after completing the order
        empyty_page = self.browser.find_element(
            By.CLASS_NAME, 'empty-base-page'
        ).text

        self.assertIn('Nenhum pedido feito.', empyty_page)

        # Go to the completed orders page
        self.browser.get(self.live_server_url + reverse(
            'staff:ordered_complete'
        ))

        # Verify that the completed order is not showing as "no orders made"
        body = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertNotIn('Nenhum pedido feito.', body.text)

        # Confirm that the completed order title is displayed correctly
        product_title = self.browser.find_element(
            By.CLASS_NAME, 'order-title'
        ).text

        self.assertEqual(product_title, 'Pedido #1')
