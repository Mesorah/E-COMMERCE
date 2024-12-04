from django.test import TestCase
from home.models import Products
from django.contrib.auth.models import User


class TestModelProducts(TestCase):
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

    def test_if_products_returns_correct_name(self):
        name = 'Test Product'

        self.assertEqual(str(self.product), name)
