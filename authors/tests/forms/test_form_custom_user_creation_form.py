from django.test import TestCase

from authors.forms import CustomUserCreationForm
from authors.models import UserProfile


class TestModelUserProfile(TestCase):
    def setUp(self):
        self.data = {
            'username': 'Test',
            'email': 'Test@gmail.com',
            'cpf': '04887398026',
            'password1': 'TestingTest123',
            'password2': 'TestingTest123',
        }

        self.form = CustomUserCreationForm(self.data)

        return super().setUp()

    def test_custom_user_creation_forms_is_valid(self):
        self.assertTrue(self.form.is_valid())

    def test_custom_user_creation_cpf_is_not_valid(self):
        self.data['cpf'] = '12345678901'

        self.assertFalse(self.form.is_valid())
        self.assertIn('cpf', self.form.errors)

    def test_custom_user_creation_user_is_created(self):
        user = self.form.save(commit=False)

        self.assertIsNone(user.id)

        self.form.save()

        self.assertIsNotNone(user.id)
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(user.username, 'Test')

    def test_custom_user_creation_user_profile_is_created(self):
        profile = self.form.save(commit=False)

        self.assertIsNone(profile.id)

        self.form.save()

        self.assertIsNotNone(profile.id)
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(profile.username, 'Test')

    def test_custom_user_creation_forms_invalid_username(self):
        self.data['username'] = 'ab'

        self.assertFalse(self.form.is_valid())
        self.assertIn('username', self.form.errors)
        self.assertIn(
            'Nome precisa de pelo menos 3 caracteres',
            self.form.errors['username']
        )
