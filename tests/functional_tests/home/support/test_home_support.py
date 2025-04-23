from django.urls import reverse
from selenium.webdriver.common.by import By

from tests.functional_tests.authors.base import AuthorsBaseFunctionalTest


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
