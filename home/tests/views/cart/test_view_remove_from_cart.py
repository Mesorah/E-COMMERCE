from django.test import TestCase
from django.urls import resolve, reverse

from home import views
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
                                   kwargs={'pk': '1'}))

        self.assertEqual(response.func.view_class, views.RemoveFromCartView)

    def test_if_home_remove_from_cart_is_get(self):
        self.client.post(
            reverse('home:add_to_cart', kwargs={'pk': '1'})
        )

        response = self.client.get(reverse(
            'home:remove_from_cart', kwargs={'pk': '1'}
        ))

        self.assertEqual(response.status_code, 405)

    def test_remove_from_cart(self):
        self.client.post(
            reverse('home:add_to_cart', kwargs={'pk': '1'})
        )

        response = self.client.post(reverse(
            'home:remove_from_cart', kwargs={'pk': '1'}
        ))

        self.assertRedirects(response, reverse('home:cart_detail'))
