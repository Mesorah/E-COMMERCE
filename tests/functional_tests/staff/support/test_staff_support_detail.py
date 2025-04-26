from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.functional_tests.staff.base import StaffBaseFunctionalTest


class StaffSupportDetailFunctionalTest(StaffBaseFunctionalTest):
    def setUp(self):
        super().setUp()

        self.super_user = self.login_user(
            reverse_url='staff:support_staff', return_super_user=True
        )

    def test_staff_support_detail_is_correct(self):
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

        # Click the "View" button
        visualization_button = self.browser.find_element(
            By.XPATH, "//a[text()='Visualizar']"
        )

        visualization_button.click()

        # Wait until the support detail text appears
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'support-text')
            )
        )

        # Check if the correct username is displayed
        username = self.browser.find_element(
            By.CLASS_NAME, 'support-text'
        ).text

        self.assertEqual('Nome: test - 04887398026', username)
