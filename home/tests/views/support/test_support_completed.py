from django.test import TestCase
from django.urls import resolve, reverse

from home import views
from utils.for_tests.base_for_authentication import register_user


class TestSupportCompleted(TestCase):
    def setUp(self):
        register_user()
        self.client.login(username='Test', password='Test')

        return super().setUp()

    def test_if_home_support_completed_load_the_correct_view(self):
        response = resolve(reverse('home:support_completed'))

        self.assertEqual(response.func.view_class, views.SupportCompleted)

    def test_if_home_support_completed_load_the_correct_template(self):
        response = self.client.get(reverse('home:support_completed'))

        self.assertTemplateUsed(response, 'home/pages/support_completed.html')

    def test_if_home_support_completed_returns_200(self):
        response = self.client.get(reverse('home:support_completed'))

        self.assertEqual(response.status_code, 200)
