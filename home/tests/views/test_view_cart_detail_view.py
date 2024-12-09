from utils.for_tests.base_for_authentication import register_user
from utils.for_tests.base_for_create_itens import (
    create_product, create_cart, create_cart_item
)
from django.urls import reverse, resolve
from home.models import CartItem
from django.test import TestCase
from home import views
import pytest


@pytest.mark.test
class TestViewRemoveCartDetailView(TestCase):
    def setUp(self):
        self.user = register_user()
        self.client.login(username='Test', password='Test')

        self.product = create_product(self.user)
        self.product2 = create_product(self.user, name='teste product 2')
        self.cart = create_cart(self.user)
        self.cart_item = create_cart_item(self.cart, self.product)
        self.cart_item2 = create_cart_item(self.cart, self.product2)

        return super().setUp()

    def test_if_home_cart_detail_view_load_the_correct_view(self):
        response = resolve(reverse('home:cart_detail',))

        # self.assertEqual(response.func.view_class, views.deta)

        self.assertEqual(response.func, views.cart_detail_view)

    def test_if_home_cart_detail_view_load_the_correct_template(self):
        response = self.client.get(reverse('home:cart_detail'))

        self.assertTemplateUsed(response, 'home/pages/cart_detail.html')

    def test_item_deletion_removes_item_from_cart(self):
        cart_items = CartItem.objects.filter(
            cart=self.cart
        )

        self.assertEqual(cart_items.count(), 2)

        self.cart_item2.quantity = 0
        self.cart_item2.save()

        response = self.client.get(reverse('home:cart_detail'))

        cart_items = CartItem.objects.filter(cart=self.cart)

        self.assertEqual(cart_items.count(), 1)

        self.assertEqual(response.status_code, 302)
