from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.functional_tests.authors.base import AuthorsBaseFunctionalTest
from utils.for_tests.base_for_authentication import register_user


class SupportFunctionalTest(AuthorsBaseFunctionalTest):
    def get_questions_and_answers(self):
        expected_args = {
            'O que é este site?': 'Este é um site de perguntas frequentes para ajudar os usuários a encontrar respostas rápidas.', # noqa E501
            'Como posso entrar em contato com o suporte?': 'Você pode entrar em contato conosco através do formulário na página de contato.', # noqa E501
            'Como faço para criar uma conta?': 'Você pode criar uma conta clicando no botão "Registrar" no topo da página.', # noqa E501
            'Esqueci minha senha. O que fazer?': 'Na página de login, clique em "Esqueci minha senha" e siga as instruções para redefinir.' # noqa E501
        }

        return expected_args

    def get_question_and_answer_is_correct(self, **expected_args):
        for question_text, answer_text in expected_args.items():

            # View a question
            question = self.browser.find_element(
                By.XPATH, f"//button[text()='{question_text}']"
            )

            # Click in the questions
            question.click()

            # View a answer
            answer = self.browser.find_element(
                By.XPATH,
                f"//p[text()='{answer_text}']"
            )

            # The answer is displayed
            self.assertTrue(answer.is_displayed())

        return question, answer

    def test_home_faq_displays_correct_number_of_questions_and_answers(self):
        # User view the page
        self.browser.get(self.live_server_url + reverse('home:faq'))

        # He clicks in the questions
        questions = self.browser.find_elements(By.CLASS_NAME, 'faq-question')

        expected_args = self.get_questions_and_answers()
        self.get_question_and_answer_is_correct(**expected_args)

        self.assertEqual(len(questions), 4)

    def test_home_support_is_correct(self):
        register_user()

        # Go to the login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Find username and password input fields
        username_id = self.browser.find_element(By.ID, 'id_username')
        password_id = self.browser.find_element(By.ID, 'id_password')

        # Fill in login credentials and submit the form
        username_id.send_keys('Test')
        password_id.send_keys('Test')
        password_id.send_keys(Keys.ENTER)

        # Wait until the products container appears after login
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'products-container')
            )
        )

        # User navigates to the support page
        self.browser.get(self.live_server_url + reverse('home:support_client'))

        # User sees the placeholder in the question field
        field = self.browser.find_element(By.ID, 'question')
        placeholder = field.get_attribute('placeholder')

        self.assertEqual('Escreva sua dúvida aqui...', placeholder)

        # User types a question into the field
        field.send_keys('Test question')

        # User clicks the submit button
        submit_button = self.browser.find_element(
            By.CLASS_NAME, 'submit-button'
        )
        submit_button.click()

        # Wait until the support message appears after submitting the question
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'support_message')
            )
        )

        # Check if the success message is displayed correctly
        support_message = self.browser.find_element(
            By.CLASS_NAME, 'support_message'
        ).text

        self.assertEqual(
            ('Sua pergunta foi enviada, quando respondermos '
             'enviaremos para o seu e-mail'),
            support_message
        )
