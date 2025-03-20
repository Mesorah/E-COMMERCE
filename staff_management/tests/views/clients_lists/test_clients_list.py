from django.test import TestCase
from django.urls import resolve, reverse

from staff_management import views
from utils.for_tests.base_for_authentication import (  # noqa E501
    register_super_user,
    register_user,
)


class TestClientsList(TestCase):
    def setUp(self):
        register_super_user()

        self.client.login(username='test', password='123')

        register_user()

        return super().setUp()

    def test_if_staff_clients_list_load_the_correct_view(self):
        response = resolve(reverse('staff:clients'))

        self.assertEqual(response.func.view_class, views.ClientsListView)

    def test_user_without_permission_redirects_from_staff_clients_list(self):
        self.client.login(username='Test', password='Test')

        response = self.client.get(reverse('staff:clients'))

        self.assertEqual(response.status_code, 302)

    def test_user_with_permissions_accesses_clients_list_and_gets_200(self):
        response = self.client.get(reverse('staff:clients'))

        self.assertEqual(response.status_code, 200)

    def test_if_staff_clients_list_have_the_correct_template(self):
        response = self.client.get(reverse('staff:clients'))

        self.assertTemplateUsed(
            response,
            'staff_management/pages/clients.html'
        )
