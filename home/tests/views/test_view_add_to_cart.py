from utils.for_tests.base_for_authentication import register_user
from utils.for_tests.base_for_create_itens import (
    create_product, create_cart, create_cart_item
)
from django.contrib.messages import get_messages
from django.urls import reverse, resolve
from home.models import CartItem
from django.test import TestCase
from home import views


class TestViewAddToCart(TestCase):
    def setUp(self):
        self.user = register_user()

        self.client.login(username='Test', password='Test')

        self.product = create_product(self.user)
        self.product2 = create_product(self.user, name='teste product 2')
        self.cart = create_cart(self.user)
        self.cart_item = create_cart_item(self.cart, self.product)

        return super().setUp()

    def test_if_home_add_to_cart_load_the_correct_view(self):
        response = resolve(reverse('home:add_to_cart', kwargs={'id': '1'}))

        self.assertEqual(response.func.view_class, views.AddToCartView)

    def test_if_home_add_to_cart_is_get(self):
        response = self.client.get(reverse('home:add_to_cart',
                                           kwargs={'id': '2'}))

        cart_item = CartItem.objects.filter(
            cart=self.cart
        )

        products = cart_item.all()

        self.assertEqual(products.count(), 1)

        self.assertEqual(response.status_code, 405)  # Navegador recusa

    def test_if_home_add_to_cart_is_post(self):
        response = self.client.post(reverse('home:add_to_cart',
                                            kwargs={'id': '2'}))

        cart_item = CartItem.objects.filter(
            cart=self.cart
        )

        products = cart_item.all()

        self.assertEqual(products.count(), 2)

        self.assertEqual(response.status_code, 302)

    def test_if_add_to_cart_stock_is_not_enough(self):
        response = self.client.post(reverse(
            'home:add_to_cart',
            kwargs={'id': '2'}),
            data={'quantity': '10'},
            follow=True
        )

        self.assertRedirects(response, reverse(
            'home:view_page',
            kwargs={'pk': '2'}
            )
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            'Não temos essa quantidade em estoque!'
        )
