from django.test import TestCase
from django.urls import resolve, reverse

from home import views


class TestHome(TestCase):
    def test_home_index_load_the_correct_view(self):
        response = resolve(reverse('home:index'))

        self.assertEqual(response.func.view_class, views.HomeListView)

    def test_home_index_load_the_correct_template(self):
        response = self.client.get(reverse('home:index'))

        self.assertTemplateUsed(response, 'global/pages/base_page.html')

    def test_home_index_returns_200(self):
        response = self.client.get(reverse('home:index'))

        self.assertEqual(response.status_code, 200)
