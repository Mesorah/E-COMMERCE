from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.functional_tests.staff.base import StaffBaseFunctionalTest


class StaffSupportDeleteFunctionalTest(StaffBaseFunctionalTest):
    def setUp(self):
        super().setUp()

        self.super_user = self.login_user(
            reverse_url='staff:support_staff', return_super_user=True
        )

    def test_staff_support_delete_is_correct(self):
        # Create a question to be displayed
        self.create_question()

        # Access the staff support view page
        self.browser.get(self.live_server_url + reverse(
            'staff:support_view_staff'
        ))

        # Wait for the support text to appear
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'support-text')
            )
        )

        # Find and click the "Delete" button
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

        # Check if the empty message is displayed
        empty_page = self.browser.find_element(
            By.CLASS_NAME, 'empty-base-page'
        ).text

        self.assertEqual('Nenhuma dúvida recebida.', empty_page)
