from django.test import TestCase
from django.urls import reverse


class TestHome(TestCase):
    def test_if_home_returns_200(self):
        response = self.client.get(reverse('home:index'))

        self.assertEqual(response.status_code, 200)
