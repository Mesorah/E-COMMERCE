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

        return super().setUp()

    def test_if_the_correct_login_is_redirected(self):
        data = {
            'username': 'Test',
            'password': 'Test'
        }

        response = self.client.post(reverse('authors:login'), data=data)

        self.assertEqual(response.status_code, 302)
