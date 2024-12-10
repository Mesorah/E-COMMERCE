import pytest
from django.test import TestCase
from django.urls import resolve, reverse

from authors import views
from utils.for_tests.base_for_authentication import (  # noqa E501
    register_user,
    register_user_profile,
)


@pytest.mark.test
class TestAuthorPasswordChangeView(TestCase):
    def setUp(self):
        self.user = register_user()
        self.profile = register_user_profile(self.user)

        self.client.login(username='Test', password='Test')

        self.data = {
            'old_password': 'Test',
            'new_password1': 'TestingChange',
            'new_password2': 'TestingChange',
        }

        return super().setUp()

    def test_if_author_password_change_load_the_correct_view(self):
        response = resolve(reverse('authors:change_password'))

        self.assertEqual(
            response.func.view_class,
            views.AuthorPasswordChangeView
        )

    def test_if_the_correct_password_change_is_redirected(self):
        response = self.client.post(reverse('authors:change_password'),
                                    data=self.data)

        self.assertEqual(response.status_code, 302)

    def test_if_author_password_change_context_is_correct(self):
        response = self.client.get(
            reverse('authors:change_password'),
            data=self.data
        )

        context = response.context

        self.assertIn('title', context)
        self.assertIn(context['title'], 'Alterar senha')

        self.assertIn('msg', context)
        self.assertIn(context['msg'], 'Atualizar senha')
