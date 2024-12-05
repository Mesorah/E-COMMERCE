from django.test import TestCase
from django.urls import reverse
from utils.for_tests.base_for_authentication import (
    register_user,
    register_user_profile,
)


class TestAuthorLogoutView(TestCase):
    def setUp(self):
        self.user = register_user()
        self.profile = register_user_profile(self.user)

        self.client.login(username='Test', password='Test')

        return super().setUp()

    def test_if_the_correct_logout_is_redirected(self):
        response = self.client.post(reverse('authors:logout'))

        self.assertEqual(response.status_code, 302)
