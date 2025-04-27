from django.test import TestCase
from django.urls import resolve, reverse

from home import views
from utils.for_tests.base_for_authentication import register_user


class TestSupportClient(TestCase):
    def setUp(self):
        register_user()

        self.client.login(username='Test', password='Test')

        return super().setUp()

    def test_home_support_client_load_the_correct_view(self):
        response = resolve(reverse('home:support_client'))

        self.assertEqual(response.func.view_class, views.SupportClient)

    def test_home_support_client_load_the_correct_template(self):
        response = self.client.get(reverse('home:support_client'))

        self.assertTemplateUsed(response, 'home/pages/support.html')

    def test_home_support_client_returns_200(self):
        response = self.client.get(reverse('home:support_client'))

        self.assertEqual(response.status_code, 200)

    def test_home_support_client_returns_302(self):
        response = self.client.post(reverse('home:support_client'))

        self.assertEqual(response.status_code, 302)
