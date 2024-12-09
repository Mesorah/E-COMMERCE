from django.test import TestCase
from utils.for_tests.base_for_authentication import register_user
from utils.for_tests.base_for_create_itens import create_cart


class TestModelCart(TestCase):
    def setUp(self):
        self.user = register_user()

        self.client.login(username='Test', password='Test')

        self.cart = create_cart(self.user)

        return super().setUp()

    def test_if_cart_returns_correct_name(self):
        name = 'Carrinho do Test'

        self.assertEqual(str(self.cart), name)
