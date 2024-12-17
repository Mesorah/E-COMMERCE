from django.test import TestCase
from django.urls import resolve, reverse

from staff_management import views
from utils.for_tests.base_for_authentication import register_user
from utils.for_tests.base_for_setup import create_ordered_setup


class TestClientsListOrdered(TestCase):
    def setUp(self):
        self.ordered = create_ordered_setup()
        self.client.login(username='test', password='123')

        return super().setUp()

    def test_if_staff_clients_list_ordered_load_the_correct_view(self):
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

    def test_user_without_permission_redirects_from_staff_client_ordered(self):
        register_user()

        self.client.login(username='Test', password='Test')

        response = self.client.get(
            reverse(
                'staff:client_list_ordered',
                kwargs={'pk': '1'}
                )
            )

        self.assertEqual(response.status_code, 302)

    def test_user_with_permissions_accesses_clients_list_and_gets_200(self):
        self.client.login(username='test', password='123')

        response = self.client.get(
            reverse(
                'staff:client_list_ordered',
                kwargs={'pk': '1'}
                )
            )

        self.assertEqual(response.status_code, 200)

    def test_if_staff_clients_list_have_the_correct_template(self):
        self.client.login(username='test', password='123')

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
