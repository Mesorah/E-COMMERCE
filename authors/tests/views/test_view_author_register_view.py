from django.test import TestCase
from django.urls import reverse


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

    def test_if_the_correct_register_is_redirected(self):
        response = self.client.post(
            reverse('authors:register'),
            data=self.data
        )

        self.assertEqual(response.status_code, 302)

    def test_if_context_is_correct(self):
        response = self.client.get(
            reverse('authors:register'),
            data=self.data
        )

        context = response.context

        self.assertIn('title', context)
        self.assertIn(context['title'], 'Register')

        self.assertIn('msg', context)
        self.assertIn(context['msg'], 'Registre-se')
