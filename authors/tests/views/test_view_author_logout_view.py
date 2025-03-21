from django.test import TestCase
from django.urls import resolve, reverse

from authors import views
from utils.for_tests.base_for_authentication import register_user


class TestAuthorLogoutView(TestCase):
    def setUp(self):
        self.user = register_user()

        self.client.login(username='Test', password='Test')

        return super().setUp()

    def test_if_author_logout_load_the_correct_view(self):
        response = resolve(reverse('authors:logout'))

        self.assertEqual(response.func.view_class, views.AuthorLogoutView)

    def test_if_the_correct_logout_is_redirected(self):
        response = self.client.post(reverse('authors:logout'))

        self.assertEqual(response.status_code, 302)
