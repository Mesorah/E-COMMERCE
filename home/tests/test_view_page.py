from django.test import TestCase
from django.urls import reverse
from home.models import Products
from django.contrib.auth.models import User


class TestViewPage(TestCase):
    def setUp(self):
        credentials = {
            'username': 'Test',
            'password': 'Test'
        }

        self.user = User.objects.create_user(**credentials)

        self.client.login(**credentials)

        self.product = Products.objects.create(
            name='Test Product',
            price=150,
            description='Test',
            user=self.user
        )

        return super().setUp()

    def test_if_page_retuns_200(self):
        response = self.client.get(
            reverse(
                'home:view_page',
                kwargs={'id': '1'}
                )
            )

        self.assertEqual(response.status_code, 200)

    def test_if_page_retuns_404(self):
        response = self.client.get(
            reverse(
                'home:view_page',
                kwargs={'id': '2'}
                )
            )

        self.assertEqual(response.status_code, 404)
