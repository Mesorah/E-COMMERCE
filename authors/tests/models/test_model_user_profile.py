from django.test import TestCase
from django.contrib.auth.models import User
from authors.models import UserProfile
from django.core.exceptions import ValidationError


class TestModelUserProfile(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='Test',
            password='Test'
        )

        self.profile = UserProfile.objects.create(
            user=self.user,
            cpf='04887398026'
        )

        return super().setUp()

    def test_if_profile_returns_correct_name(self):
        completed_sentence = 'Test - 04887398026'

        self.assertEqual(str(self.profile), completed_sentence)

    def test_if_cpf_is_not_valid(self):
        self.profile.cpf = '12345678901'

        with self.assertRaises(ValidationError) as cm:
            self.profile.full_clean()

        self.assertIn('CPF inválido.', str(cm.exception))

    def test_if_cpf_is_valid(self):
        self.profile.full_clean()
