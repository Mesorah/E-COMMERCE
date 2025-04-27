from django.test import TestCase
from django.urls import resolve, reverse

from staff_management import views
from utils.for_tests.base_for_create_itens import create_ordered


class StaffOrderedSearchTest(TestCase):
    def test_staff_ordered_search_uses_correct_view_function(self):
        resolved = resolve(reverse('staff:staff_ordered_search'))
        self.assertIs(
            resolved.func.view_class,
            views.StaffOrderedSearchListView
        )

    def test_staff_ordered_search_loads_corret_template(self):
        response = self.client.get(
            reverse('staff:staff_ordered_search') + '?q=teste'
        )

        self.assertTemplateUsed(
            response,
            'staff_management/pages/search_ordereds.html'
        )

    def test_staff_ordered_search_raises_404_if_no_search_term(self):
        url = reverse('staff:staff_ordered_search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_staff_ordered_search_term_is_on_page_title_and_escaped(self):
        url = reverse('staff:staff_ordered_search') + '?q=<Teste>'
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;&lt;Teste&gt;&quot;',
            response.content.decode('utf-8')
        )

    def test_staff_ordered_search_is_found(self):
        title1 = 'This is ordered one'
        ordered1 = create_ordered(first_name=title1)

        search_url = reverse('staff:staff_ordered_search')
        response = self.client.get(f'{search_url}?q={title1}')

        title2 = 'This is ordered two'
        ordered2 = create_ordered(first_name=title2)

        search_url = reverse('staff:staff_ordered_search')
        response = self.client.get(f'{search_url}?q={title2}')

        self.assertNotEqual('This is ordered one', response.context['ordered'])

        self.assertEqual(
            str(response.context['ordered']),
            '2: This is ordered two Test Last'
        )

        self.assertIn(ordered2, response.context['ordereds'])
        self.assertNotIn(ordered1, response.context['ordereds'])

    def test_staff_ordered_search_is_not_found(self):
        title = 'This is test'
        create_ordered(first_name=title)

        search_url = reverse('staff:staff_ordered_search')
        response = self.client.get(f'{search_url}?q={'Testing'}')

        self.assertIn(
            'No Ordered found here',
            response.content.decode('utf-8')
        )
