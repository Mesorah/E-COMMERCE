from django.test import TestCase
from utils.for_tests.base_for_authentication import register_user
from utils.for_tests.base_for_create_itens import create_product


class TestModelProducts(TestCase):
    def setUp(self):
        self.user = register_user()

        self.client.login(username='Test', password='Test')

        self.product = create_product(self.user)

        return super().setUp()

    def test_if_products_returns_correct_name(self):
        name = 'Test Product'

        self.assertEqual(str(self.product), name)
