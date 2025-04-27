from django.core.exceptions import ValidationError
from django.test import TestCase

from utils.for_tests.base_for_authentication import register_user


class TestModelUserProfile(TestCase):
    def setUp(self):
        self.user = register_user()

        return super().setUp()

    def test_profile_returns_correct_name(self):
        completed_sentence = 'Test - 21257890000'

        self.assertEqual(str(self.user), completed_sentence)

    def test_cpf_is_not_valid(self):
        self.user.cpf = '12345678901'

        with self.assertRaises(ValidationError) as cm:
            self.user.full_clean()

        self.assertIn('CPF inválido.', str(cm.exception))

    def test_cpf_is_valid(self):
        self.user.full_clean()
