from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.functional_tests.authors.base import AuthorsBaseFunctionalTest


class AuthorsRegisterFunctionalTest(AuthorsBaseFunctionalTest):
    def fill_form_dummy_data(
            self, form, override_field=None, override_value=None
    ):
        fields_data = {
            'id_username': 'dummyuser',
            'id_email': 'dummy@email.com',
            'id_cpf': '11111111111',
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

    def get_errors(self, errors):
        errors_messages = []

        for error in errors:
            errors_messages.append(error.text)

        return errors_messages

    def test_authors_register_username_message_error(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.browser.find_element(By.CLASS_NAME, 'author-form')
        self.fill_form_dummy_data(form, 'id_username', 'me')
        errors = self.browser.find_elements(By.CLASS_NAME, 'error-message')
        errors_messages = self.get_errors(errors)
        self.assertIn(
            'O username precisa de pelo menos 3 caracteres', errors_messages
        )

    # test placeholder
    # test mensage error
