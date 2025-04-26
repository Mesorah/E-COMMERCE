from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.functional_tests.staff.base import StaffBaseFunctionalTest


class StaffSupportViewFunctionalTest(StaffBaseFunctionalTest):
    def setUp(self):
        super().setUp()

        self.super_user = self.login_user(
            reverse_url='staff:support_staff', return_super_user=True
        )

    def test_staff_support_view_is_correct(self):
        # Access the client support page
        self.browser.get(self.live_server_url + reverse('home:support_client'))

        # Find the question field and submit a question
        field = self.browser.find_element(By.ID, 'question')

        field.send_keys('Test question')

        # Find and click the submit button
        submit_button = self.browser.find_element(
            By.CLASS_NAME, 'submit-button'
        )

        submit_button.click()

        # Wait for the success message to appear
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'support_message')
            )
        )

        # Access the staff support view page
        self.browser.get(self.live_server_url + reverse(
            'staff:support_view_staff'
        ))

        # Wait for the support text to load
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'support-text')
            )
        )

        # Find the username text and check if it's correct
        username = self.browser.find_element(
            By.CLASS_NAME, 'support-text'
        ).text

        self.assertEqual('Nome: test - 04887398026', username)
