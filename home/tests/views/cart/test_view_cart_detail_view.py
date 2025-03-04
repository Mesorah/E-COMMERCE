from django.test import TestCase
from django.urls import resolve, reverse

from home import views
from home.models import CartItem
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

    # USAR SESSION
    # def test_item_deletion_removes_item_from_cart(self):
    #     cart_items = CartItem.objects.filter(
    #         user=self.user_profile
    #     )

    #     self.assertEqual(cart_items.count(), 2)

    #     self.cart_item2.quantity = 0
    #     self.cart_item2.save()

    #     self.fail(self.client.session['cart'])

    #     response = self.client.get(reverse('home:cart_detail'))

    #     cart_items = CartItem.objects.filter(user=self.user_profile)

    #     self.assertEqual(cart_items.count(), 1)

    #     self.assertEqual(response.status_code, 302)
