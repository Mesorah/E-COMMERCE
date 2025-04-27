from django.test import TestCase

from utils.for_tests.base_for_authentication import register_user
from utils.for_tests.base_for_create_itens import (  # noqa E501
    create_cart_item,
    create_product,
)


class TestModelCartItem(TestCase):
    def setUp(self):
        self.user = register_user()
        self.client.login(username='Test', password='Test')

        self.product = create_product(self.user)
        self.cart_item = create_cart_item(self.product, self.user)

        return super().setUp()

    def test_cart_item_returns_correct_name(self):
        name = '1 x Test Product no carrinho'

        self.assertEqual(str(self.cart_item), name)
