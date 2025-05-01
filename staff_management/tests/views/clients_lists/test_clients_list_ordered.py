from django.test import TestCase
from django.urls import resolve, reverse

from staff_management import views
from utils.for_tests.base_for_authentication import (  # noqa E501
    register_super_user,
    register_user,
)
from utils.for_tests.base_for_create_itens import create_product


class TestClientsListOrdered(TestCase):
    def setUp(self):
        super_user = register_super_user()
        self.client.login(username='test', password='123')

        create_product(super_user)

        self.user = register_user()

        return super().setUp()

    def test_staff_clients_list_ordered_load_the_correct_view(self):
        response = resolve(
            reverse(
                'staff:client_list_ordered',
                kwargs={'pk': '1'}
                )
            )

        self.assertEqual(
            response.func.view_class,
            views.ClientListOrderedDetailView
        )

    def test_staff_clients_list_have_the_correct_template(self):
        response = self.client.get(
            reverse(
                'staff:client_list_ordered',
                kwargs={'pk': '1'}
                )
            )

        self.assertTemplateUsed(
            response,
            'staff_management/pages/ordered.html'
        )

    def test_user_without_permission_redirects_from_staff_client_ordered(self):
        self.client.login(username='Test', password='Test')

        response = self.client.get(
            reverse(
                'staff:client_list_ordered',
                kwargs={'pk': '1'}
                )
            )

        self.assertEqual(response.status_code, 302)

    def test_user_with_permissions_accesses_clients_list_and_gets_200(self):
        response = self.client.get(
            reverse(
                'staff:client_list_ordered',
                kwargs={'pk': '1'}
                )
            )

        self.assertEqual(response.status_code, 200)
