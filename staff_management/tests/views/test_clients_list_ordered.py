from django.test import TestCase
from django.urls import resolve, reverse

from home.models import CartItem
from staff_management import views
from utils.for_tests.base_for_authentication import (  # noqa E501
    register_super_user,
    register_user,
)
from utils.for_tests.base_for_create_itens import (
    create_cart,
    create_cart_item,
    create_ordered,
    create_product,
)


class TestClientsListOrdered(TestCase):
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

    def test_if_staff_clients_list_ordered_load_the_correct_view(self):
        response = resolve(
            reverse(
                'staff:client_list_ordered',
                kwargs={'id': '1'}
                )
            )

        # self.assertEqual(response.func.view_class, views.HomeListView)
        self.assertEqual(response.func, views.client_list_ordered)

    def test_user_without_permission_redirects_from_staff_client_ordered(self):
        register_user()

        self.client.login(username='Test', password='Test')

        response = self.client.get(
            reverse(
                'staff:client_list_ordered',
                kwargs={'id': '1'}
                )
            )

        self.assertEqual(response.status_code, 302)

    def test_user_with_permissions_accesses_clients_list_and_gets_200(self):
        self.client.login(username='test', password='123')

        response = self.client.get(
            reverse(
                'staff:client_list_ordered',
                kwargs={'id': '1'}
                )
            )

        self.assertEqual(response.status_code, 200)

    def test_if_staff_clients_list_have_the_correct_template(self):
        self.client.login(username='test', password='123')

        response = self.client.get(
            reverse(
                'staff:client_list_ordered',
                kwargs={'id': '1'}
                )
            )

        self.assertTemplateUsed(
            response,
            'staff_management/pages/ordered.html'
        )
