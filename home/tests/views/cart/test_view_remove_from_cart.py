from django.test import TestCase
from django.urls import resolve, reverse

from home import views
from home.models import CartItem
from utils.for_tests.base_for_setup import create_cart_item_setup


class TestViewRemoveFromCart(TestCase):
    def setUp(self):
        (self.product,
         self.product2,
         self.cart_item,
         self.cart_item2,
         self.user_profile) = create_cart_item_setup(
            product_2=True
        )

        self.client.login(username='Test', password='Test')

        return super().setUp()

    def test_if_home_remove_from_cart_load_the_correct_view(self):
        response = resolve(reverse('home:remove_from_cart',
                                   kwargs={'id': '1'}))

        self.assertEqual(response.func.view_class, views.RemoveFromCartView)

    def test_if_home_remove_from_cart_is_get(self):
        cart_item = CartItem.objects.filter(
            user=self.user_profile
        )

        products = cart_item.all()

        self.assertEqual(products.count(), 2)

        response = self.client.get(
            reverse('home:remove_from_cart', kwargs={'id': '1'}),
            data={'quantity-to-remove': 1}
        )

        cart_item = CartItem.objects.filter(
            user=self.user_profile
        )

        products = cart_item.all()

        self.assertEqual(products.count(), 2)

        self.assertEqual(response.status_code, 405)

    # USAR SESSION
    # def test_if_home_remove_from_cart_is_post(self):
    #     cart_item = CartItem.objects.filter(
    #         user=self.user_profile
    #     )

    #     products = cart_item.all()

    #     self.assertEqual(products.count(), 2)

    #     response = self.client.post(
    #         reverse('home:remove_from_cart', kwargs={'id': '1'}),
    #         data={'quantity-to-remove': 1}
    #     )

    #     cart_item = CartItem.objects.filter(
    #         user=self.user_profile
    #     )

    #     products = cart_item.all()

    #     self.assertEqual(products.count(), 1)

    #     self.assertEqual(response.status_code, 302)

    # USAR SESSION
    # def test_if_home_remove_from_cart_cart_item_quantity_is_less_than_0(self):
    #     cart_item = CartItem.objects.filter(
    #         user=self.user_profile
    #     ).first()

    #     cart_item.quantity = 10
    #     cart_item.save()

    #     self.product.stock = 10
    #     self.product.save()

    #     self.assertEqual(self.product.stock, 10)

    #     response = self.client.post(
    #         reverse('home:remove_from_cart', kwargs={'id': '1'}),
    #         data={'quantity-to-remove': 1}
    #     )

    #     cart_item = CartItem.objects.filter(
    #         user=self.user_profile
    #     )

    #     products = cart_item.all()

    #     self.assertEqual(products.count(), 2)

    #     self.assertEqual(response.status_code, 302)
