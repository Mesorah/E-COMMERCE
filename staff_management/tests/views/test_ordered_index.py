from django.test import TestCase
from django.urls import resolve, reverse

from home.models import CartItem
from staff_management import views
from utils.for_tests.base_for_authentication import register_super_user
from utils.for_tests.base_for_create_itens import (
    create_cart,
    create_cart_item,
    create_ordered,
    create_product,
)


class TestOrderedIndex(TestCase):
    def setUp(self):
        self.user = register_super_user()

        self.product = create_product(self.user)
        self.cart = create_cart(self.user)
        self.cart_item = create_cart_item(self.cart, self.product)
        cart_item = CartItem.objects.filter(cart=self.cart, is_ordered=False)
        self.ordered = create_ordered()
        # self.ordered.save()
        self.ordered.products.set(cart_item)

        return super().setUp()

    def test_if_staff_index_load_the_correct_view(self):
        self.client.login(username='test', password='123')
        response = resolve(reverse('staff:ordered_index'))

        self.assertEqual(response.func.view_class, views.OrderedIndexView)

    def test_if_ordered_index_load_the_correct_template(self):
        self.client.login(username='test', password='123')

        response = self.client.get(reverse('staff:ordered_index'))

        self.assertTemplateUsed(
            response,
            'staff_management/pages/ordered.html'
        )
