from django.urls import reverse
from selenium.webdriver.common.by import By

from tests.functional_tests.home.payment.base import PaymentBaseFunctionalTest


class PaymentFunctionalTest(PaymentBaseFunctionalTest):
    def setUp(self):
        super().setUp()

        self.get_product_in_cart()
        self.browser.get(self.live_server_url + reverse('home:payment'))

        self.informations = {
            'id_first_name': 'Camila',
            'id_last_name': 'Oliveira',
            'id_credit_card': '4242424242424242',
            'id_expiration_date': '09/2028',
            'id_cvv': '737',
            'id_cardholder_name': 'Camila Oliveira',
            'id_zip_code': '86390000',
            'id_neighborhood': 'Itaim Bibi',
            'id_street_name': 'Rua Joaquim Florian',
            'id_house_number': '450'
        }

    def submit_payment_form_and_get_errors(
            self, field_id, field_value, *error_messages
    ):
        self.informations[field_id] = field_value

        for current_field_id, expected_text in self.informations.items():
            field = self.browser.find_element(By.ID, current_field_id)
            field.send_keys(expected_text)

        # He send the informations
        form = self.browser.find_element(By.CLASS_NAME, 'payment-form')
        form.submit()

        # View a error
        errors = self.browser.find_elements(By.CLASS_NAME, 'error-message')

        for error_message in error_messages:
            self.assertIn(error_message, [error.text for error in errors])

    def test_home_payment_works_if_all_data_is_correctly(self):
        for field_id, expected_text in self.informations.items():
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

    def test_home_payment_credit_card_has_error(self):
        self.submit_payment_form_and_get_errors(
            'id_credit_card',
            '1234567890123456',
            'Cartão inválido.'
        )

    def test_home_payment_expiration_date_has_error(self):
        self.submit_payment_form_and_get_errors(
            'id_expiration_date',
            '0931',
            'Formato de data inválido. Use MM/AA ou MM/YYYY.',
            'Mês inválido.'
        )

    def test_home_payment_zip_code_has_error(self):
        self.submit_payment_form_and_get_errors(
            'id_zip_code',
            '12345678',
            'CEP diferente de cambará'
        )

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
