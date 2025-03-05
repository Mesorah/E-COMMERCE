from django.test import TestCase
from django.urls import resolve, reverse

from authors import views
from utils.for_tests.base_for_authentication import (  # noqa E501
    register_user,
    register_user_profile,
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

    def test_if_author_login_load_the_correct_view(self):
        response = resolve(reverse('authors:login'))

        self.assertEqual(response.func.view_class, views.AuthorLoginView)

    def test_if_the_correct_login_is_redirected(self):
        response = self.client.post(reverse('authors:login'), data=self.data)

        self.assertEqual(response.status_code, 302)

    def test_if_the_user_logged_is_redirect_to_home(self):
        self.client.post(reverse('authors:login'), data=self.data)
        response = self.client.get(reverse('authors:login'))

        self.assertRedirects(response, reverse('home:index'))

    def test_if_login_context_is_correct(self):
        response = self.client.get(reverse('authors:login'), data=self.data)

        context = response.context

        self.assertIn('title', context)
        self.assertIn(context['title'], 'Login')

        self.assertIn('msg', context)
        self.assertIn(context['msg'], 'Logue-se')
