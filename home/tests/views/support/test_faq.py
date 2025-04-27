from django.test import TestCase
from django.urls import resolve, reverse

from home import views


class TestFaq(TestCase):
    def test_home_faq_load_the_correct_view(self):
        response = resolve(reverse('home:faq'))

        self.assertEqual(response.func.view_class, views.Faq)

    def test_home_faq_load_the_correct_template(self):
        response = self.client.get(reverse('home:faq'))

        self.assertTemplateUsed(response, 'home/pages/faq.html')

    def test_home_faq_returns_200(self):
        response = self.client.get(reverse('home:faq'))

        self.assertEqual(response.status_code, 200)
