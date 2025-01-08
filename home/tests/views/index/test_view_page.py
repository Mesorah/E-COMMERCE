from django.test import TestCase
from django.urls import resolve, reverse

from home import views
from utils.for_tests.base_for_authentication import register_user
from utils.for_tests.base_for_create_itens import create_product


class TestViewPage(TestCase):
    def setUp(self):
        self.user = register_user()
        self.client.login(username='Test', password='Test')

        self.product = create_product(self.user)

        return super().setUp()

    def test_if_home_view_page_load_the_correct_view(self):
        response = resolve(reverse('home:view_page', kwargs={
            'slug': self.product.slug
        }))

        self.assertEqual(response.func.view_class, views.PageDetailView)

    def test_if_home_view_page_load_the_correct_template(self):
        response = self.client.get(reverse('home:view_page', kwargs={
            'slug': self.product.slug
        }))

        self.assertTemplateUsed(response, 'home/pages/view_page.html')

    def test_if_view_page_retuns_200(self):
        response = self.client.get(
            reverse(
                'home:view_page',
                kwargs={'slug': self.product.slug}
                )
            )

        self.assertEqual(response.status_code, 200)

    def test_if_view_page_retuns_404(self):
        response = self.client.get(
            reverse(
                'home:view_page',
                kwargs={'slug': f'{self.product.slug}-1'}
                )
            )

        self.assertEqual(response.status_code, 404)

    def test_if_is_published_is_false(self):
        product2 = create_product(
            user=self.user,
            name='Test Product2',
            is_published=False
        )

        response = self.client.get(
            reverse(
                'home:view_page',
                kwargs={'slug': product2.slug}
                )
            )

        self.assertEqual(response.status_code, 404)
