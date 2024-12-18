from django.test import TestCase

from utils.for_tests.base_for_authentication import register_user
from utils.for_tests.base_for_create_itens import create_question


class TestModelCustumerQuestion(TestCase):
    def setUp(self):
        self.user = register_user()

        self.client.login(username='Test', password='Test')

        self.question = create_question(self.user)

        return super().setUp()

    def test_if_custumer_question_returns_correct_name(self):
        name = 'Test'

        self.assertEqual(str(self.question), name)
