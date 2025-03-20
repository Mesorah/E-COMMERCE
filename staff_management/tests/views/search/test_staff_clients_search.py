from django.test import TestCase
from django.urls import resolve, reverse

from staff_management import views


class StaffClientsSearchTest(TestCase):
    def test_staff_client_search_uses_correct_view_function(self):
        resolved = resolve(reverse('staff:staff_client_search'))
        self.assertIs(
            resolved.func.view_class,
            views.StaffClientsSearchListView
        )

    def test_staff_client_search_loads_corret_template(self):
        response = self.client.get(
            reverse('staff:staff_client_search') + '?q=teste'
        )

        self.assertTemplateUsed(
            response,
            'staff_management/pages/search_clients.html'
        )

    def test_staff_client_search_raises_404_if_no_search_term(self):
        url = reverse('staff:staff_client_search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_staff_client_search_term_is_on_page_title_and_escaped(self):
        url = reverse('staff:staff_client_search') + '?q=<Teste>'
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;&lt;Teste&gt;&quot;',
            response.content.decode('utf-8')
        )
