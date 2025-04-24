from selenium.webdriver.common.by import By

from tests.functional_tests.staff.base import StaffBaseFunctionalTest
from utils.for_tests.base_for_create_itens import create_test_image_file


class StaffCreateProductFunctionalTest(StaffBaseFunctionalTest):
    def setUp(self):
        super().setUp()

        self.login_user(reverse_url='staff:add_product')

        self.informations = {
            'id_name': 'Test name',
            'id_price': '150',
            'id_description': 'This is a description test',
            'id_stock': '1',
            'id_is_published': 'True',
            'id_cover': create_test_image_file(),
        }

        # Serves for self.informations, if the variable is skipped in the tests
        self.field_id_empty = None

    def submit_product_form_and_get_errors(
            self, field_id, field_value, *error_messages
    ):
        self.informations[field_id] = field_value

        for current_field_id, expected_text in self.informations.items():
            if self.field_id_empty == field_id:
                continue

            field = self.browser.find_element(By.ID, current_field_id)
            field.send_keys(expected_text)

        # He send the informations
        form = self.browser.find_element(By.CLASS_NAME, 'crud-product-form')
        form.submit()

        # View a error
        errors = self.browser.find_elements(By.CLASS_NAME, 'error-message')

        for error_message in error_messages:
            self.assertIn(error_message, [error.text for error in errors])

    def test_staff_create_product_name_has_error(self):
        self.submit_product_form_and_get_errors(
            'id_name',
            'ab',
            'Nome de produto muito pequeno, precisa-se de pelo menos 3 caracteres.' # noqa E501
        )

    def test_staff_create_product_price_has_error(self):
        self.submit_product_form_and_get_errors(
            'id_price',
            '-1',
            'O preço do produto não pode ser menor ou igual a 0.'
        )

    def test_staff_create_product_stock_has_error(self):
        self.submit_product_form_and_get_errors(
            'id_stock',
            '-1',
            'O valor do stock não pode ser menor que 0.'
        )

    def test_staff_create_product_cover_has_error(self):
        self.field_id_empty = 'id_cover'

        self.submit_product_form_and_get_errors(
            'id_cover',
            '',
            'O cover não estar ser vazio.'
        )

    def test_staff_create_product_works_if_all_data_is_correctly(self):
        for field_id, expected_text in self.informations.items():
            field = self.browser.find_element(By.ID, field_id)

            if field_id == 'id_is_published':
                field.click()

                select = self.browser.find_element(
                    By.ID,
                    'id_is_published'
                )

                option = select.find_element(
                    By.XPATH,
                    "//option[@value='true']"
                )

                option.click()

                continue

            field.send_keys(expected_text)

    def test_staff_create_product_all_placeholders_is_correct(self):
        # View the forms placeholders
        placeholders = [
            'Nome do produto',
            'Preço do produto',
            'Descrição do produto',
            'Quantidade de estoque do produto',
        ]

        for field_id, expected_text in zip(
            self.informations.keys(), placeholders
        ):
            field = self.browser.find_element(By.ID, field_id)

            placeholder = field.get_attribute('placeholder')
            self.assertEqual(placeholder, expected_text)
