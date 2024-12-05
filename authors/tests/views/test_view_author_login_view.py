from django.test import TestCase
from django.urls import reverse
from utils.for_tests.base_for_authentication import (
    register_user,
    register_user_profile
)


class TestAuthorLoginView(TestCase):
    def setUp(self):
        self.user = register_user()
        self.profile = register_user_profile(self.user)

        self.data = {
            'username': 'Test',
            'password': 'Test'
        }

        return super().setUp()

    def test_if_the_correct_login_is_redirected(self):
        response = self.client.post(reverse('authors:login'), data=self.data)

        self.assertEqual(response.status_code, 302)

    def test_if_login_context_is_correct(self):
        response = self.client.get(reverse('authors:login'), data=self.data)

        context = response.context

        self.assertIn('title', context)
        self.assertIn(context['title'], 'Login')

        self.assertIn('msg', context)
        self.assertIn(context['msg'], 'Logue-se')
