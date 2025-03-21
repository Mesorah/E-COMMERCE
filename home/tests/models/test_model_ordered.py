from django.test import TestCase

from home.models import CartItem
from utils.for_tests.base_for_authentication import register_user
from utils.for_tests.base_for_create_itens import (
    create_cart_item,
    create_ordered,
    create_product,
)


class TestModelOrdered(TestCase):
    def setUp(self):
        self.user = register_user()
        self.client.login(username='Test', password='Test')

        self.product = create_product(self.user)
        self.cart_item = create_cart_item(self.product, self.user)
        cart_item = CartItem.objects.filter(user=self.cart_item.user)
        self.ordered = create_ordered()
        # self.ordered.save()
        self.ordered.products.set(cart_item)

        return super().setUp()

    def test_if_ordered_returns_correct_name(self):
        name = '1: Test First Test Last'

        self.assertEqual(str(self.ordered), name)

    def test_ordered_last_order_retuns_correct_number(self):
        ordered = create_ordered()

        name = '2: Test First Test Last'

        self.assertEqual(str(ordered), name)
