from utils.for_tests.base_for_authentication import register_user
from utils.for_tests.base_for_create_itens import (
    create_product, create_cart, create_cart_item
)
from django.urls import reverse, resolve
from home.models import CartItem
from django.test import TestCase
from home import views


class TestViewRemoveFromCart(TestCase):
    def setUp(self):
        self.user = register_user()

        self.client.login(username='Test', password='Test')

        self.product = create_product(self.user)
        self.product2 = create_product(self.user, name='teste product 2')
        self.cart = create_cart(self.user)
        self.cart_item = create_cart_item(self.cart, self.product)

        return super().setUp()

    def test_if_home_remove_from_cart_load_the_correct_view(self):
        response = resolve(reverse('home:remove_from_cart',
                                   kwargs={'id': '1'}))

        self.assertEqual(response.func.view_class, views.RemoveFromCartView)

    def test_if_home_remove_from_cart_is_get(self):
        response = self.client.get(reverse('home:remove_from_cart',
                                           kwargs={'id': '1'}))

        cart_item = CartItem.objects.filter(
            cart=self.cart
        )

        products = cart_item.all()

        self.assertEqual(products.count(), 1)

        self.assertEqual(response.status_code, 405)

    def test_if_home_remove_from_cart_is_post(self):
        response = self.client.post(reverse('home:remove_from_cart',
                                            kwargs={'id': '1'}))

        cart_item = CartItem.objects.filter(
            cart=self.cart
        )

        products = cart_item.all()

        self.assertEqual(products.count(), 1)

        self.assertEqual(response.status_code, 302)
