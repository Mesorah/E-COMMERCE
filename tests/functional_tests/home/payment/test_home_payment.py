from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.functional_tests.base import BaseFunctionalTest


class PaymentFunctionalTest(BaseFunctionalTest):
    def setUp(self):
        super().setUp()

        self.get_product_in_cart()

    def test_home_payment_works_if_all_data_is_correctly(self):
        # User view the page
        self.browser.get(self.live_server_url + reverse('home:payment'))

        # He saw that he was not logged in
        self.assertEqual(self.browser.title, 'Login')

        username = self.browser.find_element(By.ID, 'id_username')
        password = self.browser.find_element(By.ID, 'id_password')

        # Then logs into the site
        username.send_keys('Test')
        password.send_keys('Test')
        password.send_keys(Keys.ENTER)

        # He realized he was logged in and was redirected to Home
        self.assertEqual(self.browser.title, 'Home')

        # He goes to the payment page
        self.browser.get(self.live_server_url + reverse('home:payment'))

        # View the forms placeholders
        expected_placeholders = {
            'id_first_name': 'Seu primeiro nome',
            'id_last_name': 'Seu último nome',
            'id_credit_card': 'Número do cartão de crédito',
            'id_expiration_date': 'MM/AA ou MM/YYYY',
            'id_cvv': 'CVV',
            'id_cardholder_name': 'Nome do titular do cartão',
            'id_zip_code': 'XXXXXXXX',
            'id_neighborhood': 'Bairro',
            'id_street_name': 'Rua',
            'id_house_number': 'Número da casa',
        }

        for field_id, expected_text in expected_placeholders.items():
            field = self.browser.find_element(By.ID, field_id)
            placeholder = field.get_attribute('placeholder')
            self.assertEqual(placeholder, expected_text)

        # then it fills in your information
        informations = {
            'id_first_name': 'Camila',
            'id_last_name': 'Oliveira',
            'id_credit_card': '4242424242424242',
            'id_expiration_date': '09/2028',
            'id_cvv': '737',
            'id_cardholder_name': 'Camila Oliveira',
            'id_zip_code': '86390000',
            'id_neighborhood': 'Itaim Bibi',
            'id_street_name': 'Rua Joaquim Floriano',
            'id_house_number': '450'
        }

        for field_id, expected_text in informations.items():
            field = self.browser.find_element(By.ID, field_id)
            field.send_keys(expected_text)

        # He send the informations
        form = self.browser.find_element(By.CLASS_NAME, 'payment-form')
        form.submit()

        # The user saw that the cart emptied and his money was gone
        cart_count = self.browser.find_element(
            By.CLASS_NAME, 'cart-count'
        ).text

        self.assertEqual(cart_count, '0')
