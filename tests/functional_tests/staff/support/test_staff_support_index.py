from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.functional_tests.staff.base import StaffBaseFunctionalTest


class StaffSupportIndexFunctionalTest(StaffBaseFunctionalTest):
    def setUp(self):
        super().setUp()

        self.super_user = self.login_user(
            reverse_url='staff:support_staff', return_super_user=True
        )

        self.browser.get(self.live_server_url + reverse('staff:support_staff'))

    def test_staff_support_index_is_correct(self):
        # Find the email and answer input fields
        email_field = self.browser.find_element(
            By.ID, 'email'
        )

        answer_field = self.browser.find_element(
            By.ID, 'answer'
        )

        # Check the placeholders for the email and answer fields
        email_placeholder = email_field.get_attribute('placeholder')
        answer_placeholder = answer_field.get_attribute('placeholder')

        self.assertEqual('Escreva o email aqui...', email_placeholder)
        self.assertEqual('Escreva sua resposta aqui...', answer_placeholder)

        # Fill in the email and answer fields
        email_field.send_keys('Test e-mail')
        answer_field.send_keys('Test answer')

        # Find and click the submit button
        submit_button = self.browser.find_element(
            By.CLASS_NAME, 'submit-button'
        )
        submit_button.click()

        # Wait until the support container appears after submitting
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'support-container')
            )
        )

        # Check if the empty page message is displayed
        empty_page = self.browser.find_element(
            By.CLASS_NAME, 'empty-base-page'
        ).text

        self.assertEqual('Nenhuma dúvida recebida.', empty_page)
