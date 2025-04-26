from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.functional_tests.staff.base import StaffBaseFunctionalTest


class StaffDeleteProductFunctionalTest(StaffBaseFunctionalTest):
    def setUp(self):
        super().setUp()

        self.login_user(reverse_url='staff:index')

    def test_staff_delete_product_works(self):
        # Find and click the "Delete" butto
        delete_button = self.browser.find_element(
            By.XPATH, "//button[text()='Deletar']"
        )

        delete_button.click()

        # Accept the confirmation alert
        alert = self.browser.switch_to.alert
        alert.accept()

        # Wait until the empty page message appears
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'empty-base-page')
            )
        )

        # Check if the empty page message is correct
        empyty_page = self.browser.find_element(
            By.CLASS_NAME, 'empty-base-page'
        ).text

        self.assertIn('Nenhum produto disponível.', empyty_page)
