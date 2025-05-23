from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.functional_tests.authors.base import AuthorsBaseFunctionalTest


class AuthorsRegisterFunctionalTest(AuthorsBaseFunctionalTest):
    def setUp(self):
        super().setUp()
        self.browser.get(self.live_server_url + reverse('authors:register'))
        self.form = self.browser.find_element(By.CLASS_NAME, 'author-form')

    def fill_form_dummy_data(
            self, form, override_field=None, override_value=None
    ):
        fields_data = {
            'id_username': 'dummyuser',
            'id_email': 'dummy@email.com',
            'id_cpf': '89511513010',
            'id_password1': 'password123!',
            'id_password2': 'password123!',
        }

        if override_field and override_value:
            fields_data[override_field] = override_value

        for field_id, value in fields_data.items():
            input_field = form.find_element(By.ID, field_id)
            input_field.clear()
            input_field.send_keys(value)

        submit_button = form.find_element(By.XPATH, '//button[@type="submit"]')
        submit_button.click()

        return self.browser.find_elements(
            By.CLASS_NAME, 'error-message'
        )

    def get_errors(self, errors):
        errors_messages = []

        for error in errors:
            errors_messages.append(error.text)

        return errors_messages

    def test_authors_register_is_correct(self):
        # User has registered
        self.fill_form_dummy_data(self.form)

        # Waited for the login page to appear
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[text()='Não tem uma conta?']")
            )
        )

        # Checked if it is the correct page
        login_page = self.browser.find_element(
            By.XPATH, "//h2[text()='Logue-se']"
        ).text

        self.assertEqual(login_page, 'Logue-se')

    def test_authors_register_username_message_error(self):
        errors = self.fill_form_dummy_data(self.form, 'id_username', 'me')
        errors_messages = self.get_errors(errors)
        self.assertIn(
            'O username precisa de pelo menos 3 caracteres.', errors_messages
        )

    def test_authors_register_cpf_message_error(self):
        errors = self.fill_form_dummy_data(self.form, 'id_cpf', '11111111111')
        errors_messages = self.get_errors(errors)
        self.assertIn(
            'cpf inválido.', errors_messages
        )

    def test_authors_register_password_message_error(self):
        errors = self.fill_form_dummy_data(
            self.form, 'id_password1', 'password1!'
        )
        errors_messages = self.get_errors(errors)
        self.assertIn(
            'A password1 tem que ser igual a password2.', errors_messages
        )

    def test_authors_register_all_placeholders(self):
        self.browser.get(self.live_server_url + '/authors/register/')

        expected_placeholders = {
            'id_username': 'Ex.: Gabriel',
            'id_email': 'Ex.: exemplo@email.com',
            'id_cpf': 'Ex.: 32470317070',
            'id_password1': 'Ex.: y897`YuA/u/e',
            'id_password2': 'Ex.: y897`YuA/u/e',
        }

        for field_id, expected_text in expected_placeholders.items():
            field = self.browser.find_element(By.ID, field_id)
            placeholder = field.get_attribute('placeholder')
            self.assertEqual(placeholder, expected_text)
