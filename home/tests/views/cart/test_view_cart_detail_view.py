from django.test import TestCase
from django.urls import resolve, reverse

from home import views
from utils.for_tests.base_for_setup import create_cart_item_setup


class TestViewCartDetailView(TestCase):
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

    def test_if_home_cart_detail_view_load_the_correct_view(self):
        response = resolve(reverse('home:cart_detail',))

        self.assertEqual(response.func.view_class, views.CartDetailView)

    def test_if_home_cart_detail_view_load_the_correct_template(self):
        response = self.client.get(reverse('home:cart_detail'))

        self.assertTemplateUsed(response, 'home/pages/cart_detail.html')

    def test_cart_detail_has_a_session(self):
        self.client.post(
            reverse('home:add_to_cart', kwargs={'id': '1'})
        )

        response = self.client.get(reverse('home:cart_detail'))

        self.assertEqual(response.status_code, 200)

    def test_cart_detail_does_not_have_a_session(self):
        response = self.client.get(reverse('home:cart_detail'))

        self.assertEqual(response.status_code, 200)
