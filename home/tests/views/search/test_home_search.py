from django.test import TestCase
from django.urls import resolve, reverse

from home import views
from utils.for_tests.base_for_authentication import register_super_user
from utils.for_tests.base_for_create_itens import create_product


class HomeSearchTest(TestCase):
    def test_home_search_uses_correct_view_function(self):
        resolved = resolve(reverse('home:home_search'))
        self.assertIs(resolved.func.view_class, views.HomeSearchListView)

    def test_home_search_loads_corret_template(self):
        response = self.client.get(reverse('home:home_search') + '?q=teste')
        self.assertTemplateUsed(response, 'global/pages/search_product.html')

    def test_home_search_raises_404_if_no_search_term(self):
        url = reverse('home:home_search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_home_search_term_is_on_page_title_and_escaped(self):
        url = reverse('home:home_search') + '?q=<Teste>'
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;&lt;Teste&gt;&quot;',
            response.content.decode('utf-8')
        )

    def test_if_home_search_is_not_published(self):
        user = register_super_user()
        self.client.login(username='test', password='123')

        title = 'This is product one'
        product1 = create_product(user, name=title, is_published=False)

        search_url = reverse('home:home_search')
        response = self.client.get(f'{search_url}?q={title}')

        self.assertIn(
            'No Products found here',
            response.content.decode('utf-8')
        )

        title2 = 'This is product two'
        product2 = create_product(user, name=title2)

        search_url = reverse('home:home_search')
        response = self.client.get(f'{search_url}?q={'This is product'}')

        self.assertNotEqual('This is product one', response.context['product'])

        self.assertEqual(
            str(response.context['product']),
            'This is product two'
        )

        self.assertIn(product2, response.context['products'])
        self.assertNotIn(product1, response.context['products'])

    def test_home_search_can_find_product_by_title(self):
        user = register_super_user()
        self.client.login(username='test', password='123')

        title1 = 'This is product one'
        title2 = 'This is product two'

        product1 = create_product(user, name=title1)

        product2 = create_product(user, name=title2)

        search_url = reverse('home:home_search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=this')

        self.assertEqual(product1, response1.context['product'])
        self.assertNotEqual(product2, response1.context['product'])

        self.assertEqual(product2, response2.context['product'])
        self.assertNotEqual(product1, response2.context['product'])

        self.assertEqual(product1, response_both.context['product'])
        self.assertNotEqual(product2, response_both.context['product'])
