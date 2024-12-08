from django.test import TestCase
from django.urls import reverse
from utils.for_tests.base_for_authentication import register_user
from utils.for_tests.base_for_create_itens import create_product


class TestViewPage(TestCase):
    def setUp(self):
        self.user = register_user()
        self.client.login(username='Test', password='Test')

        self.product = create_product(self.user)

        return super().setUp()

    def test_if_view_page_retuns_200(self):
        # Erro por causa do is_published
        
        response = self.client.get(
            reverse(
                'home:view_page',
                kwargs={'pk': '1'}
                )
            )

        self.assertEqual(response.status_code, 200)

    def test_if_page_retuns_404(self):
        response = self.client.get(
            reverse(
                'home:view_page',
                kwargs={'pk': '2'}
                )
            )

        self.assertEqual(response.status_code, 404)
