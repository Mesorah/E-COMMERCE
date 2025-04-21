from django.urls import reverse
from selenium.webdriver.common.by import By

from tests.functional_tests.base import BaseFunctionalTest


class PaymentFunctionalTest(BaseFunctionalTest):
    def setUp(self):
        super().setUp()

        self.get_product_in_cart()
        self.browser.get(self.live_server_url + reverse('home:payment'))

        self.informations = {
            'id_first_name': '',
            'id_last_name': '',
            'id_credit_card': '',
            'id_expiration_date': '',
            'id_cvv': '',
            'id_cardholder_name': '',
            'id_zip_code': '',
            'id_neighborhood': '',
            'id_street_name': '',
            'id_house_number': ''
        }

    def test_home_payment_works_if_all_data_is_correctly(self):
        informations_list = [
            'Camila',
            'Oliveira',
            '4242424242424242',
            '09/2028',
            '737',
            'Camila Oliveira',
            '86390000',
            'Itaim Bibi',
            'Rua Joaquim Floriano',
            '450'
        ]

        for field_id, expected_text in zip(
            self.informations.keys(), informations_list
        ):
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

    def test_home_payment_all_placeholders(self):
        # View the forms placeholders
        placeholders = [
            'Seu primeiro nome',
            'Seu último nome',
            'Número do cartão de crédito',
            'MM/AA ou MM/YYYY',
            'CVV',
            'Nome do titular do cartão',
            'XXXXXXXX',
            'Bairro',
            'Rua',
            'Número da casa',
        ]

        for field_id, expected_text in zip(
            self.informations.keys(), placeholders
        ):
            field = self.browser.find_element(By.ID, field_id)
            placeholder = field.get_attribute('placeholder')
            self.assertEqual(placeholder, expected_text)
