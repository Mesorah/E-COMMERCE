from django.test import TestCase
from django.urls import resolve, reverse

from staff_management import views
from utils.for_tests.base_for_authentication import register_super_user
from utils.for_tests.base_for_create_itens import create_product


class StaffSearchTest(TestCase):
    def test_staff_search_uses_correct_view_function(self):
        resolved = resolve(reverse('staff:staff_search'))
        self.assertIs(resolved.func.view_class, views.StaffSearchListView)

    def test_staff_client_search_loads_corret_template(self):
        user = register_super_user()
        self.client.login(username='test', password='123')

        title = 'This is product one'
        create_product(user, name=title, is_published=False)

        search_url = reverse('staff:staff_search')
        response = self.client.get(f'{search_url}?q={title}')

        self.assertTemplateUsed(
            response,
            'global/pages/search_product.html'
        )

    def test_staff_search_is_not_published(self):
        user = register_super_user()
        self.client.login(username='test', password='123')

        title = 'This is product one'
        product1 = create_product(user, name=title, is_published=False)

        search_url = reverse('staff:staff_search')
        response = self.client.get(f'{search_url}?q={title}')

        self.assertNotIn(
            'No Products found here',
            response.content.decode('utf-8')
        )

        self.assertIn(
            'This is product one',
            str(response.context['products'])
        )

        title2 = 'This is product two'
        product2 = create_product(user, name=title2)

        search_url = reverse('staff:staff_search')
        response = self.client.get(f'{search_url}?q={'This is product'}')

        self.assertIn(
            'This is product two',
            str(response.context['products'])
        )

        self.assertIn(product2, response.context['products'])
        self.assertIn(product1, response.context['products'])
