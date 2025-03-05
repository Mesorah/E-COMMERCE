from django.test import TestCase
from django.urls import resolve, reverse

from authors import views
from utils.for_tests.base_for_authentication import register_user


class TestAuthorRegisterView(TestCase):
    def setUp(self):
        self.data = {
            'username': 'Test',
            'email': 'Test@gmail.com',
            'cpf': '04887398026',
            'password1': 'Testthetesting',
            'password2': 'Testthetesting',
        }

        return super().setUp()

    def test_if_author_register_load_the_correct_view(self):
        response = resolve(reverse('authors:register'))

        self.assertEqual(response.func.view_class, views.AuthorRegisterView)

    def test_if_the_correct_register_is_redirected(self):
        response = self.client.post(
            reverse('authors:register'),
            data=self.data
        )

        self.assertEqual(response.status_code, 302)

    def test_if_the_user_logged_is_redirect_to_home(self):
        register_user()
        self.client.login(username='Test', password='Test')
        response = self.client.get(reverse('authors:register'))

        self.assertRedirects(response, reverse('home:index'))

    def test_if_author_register_context_is_correct(self):
        response = self.client.get(
            reverse('authors:register'),
            data=self.data
        )

        context = response.context

        self.assertIn('title', context)
        self.assertIn(context['title'], 'Register')

        self.assertIn('msg', context)
        self.assertIn(context['msg'], 'Registre-se')
