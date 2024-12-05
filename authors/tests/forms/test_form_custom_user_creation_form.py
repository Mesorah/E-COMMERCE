from django.test import TestCase
from django.contrib.auth.models import User
from authors.models import UserProfile
from authors.forms import CustomUserCreationForm


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

    def test_if_the_forms_is_valid(self):
        self.assertTrue(self.form.is_valid())

    def test_if_cpf_is_not_valid(self):
        self.data['cpf'] = '12345678901'

        self.assertFalse(self.form.is_valid())
        self.assertIn('cpf', self.form.errors)

    def test_if_user_is_created(self):
        user = self.form.save(commit=False)

        self.assertIsNone(user.id)

        self.form.save()

        self.assertIsNotNone(user.id)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, 'Test')

    def test_if_user_profile_is_created(self):
        profile = self.form.save(commit=False)

        self.assertIsNone(profile.id)

        self.form.save()

        self.assertIsNotNone(profile.id)
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(profile.username, 'Test')
