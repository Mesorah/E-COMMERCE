from django.test import TestCase
from django.urls import resolve, reverse

from home import views
from utils.for_tests.base_for_authentication import register_super_user
from utils.for_tests.base_for_create_itens import create_product


class TestViewCartDetailView(TestCase):
    def setUp(self):
        user = register_super_user()
        self.client.login(username='test', password='123')

        self.product1 = create_product(user, stock=2)

        return super().setUp()

    def test_home_cart_detail_view_load_the_correct_view(self):
        response = resolve(reverse('home:cart_detail',))

        self.assertEqual(response.func.view_class, views.CartDetailView)

    def test_home_cart_detail_view_load_the_correct_template(self):
        response = self.client.get(reverse('home:cart_detail'))

        self.assertTemplateUsed(response, 'home/pages/cart_detail.html')

    def test_cart_detail_has_a_session(self):
        self.client.post(
            reverse('home:add_to_cart', kwargs={'pk': '1'})
        )

        response = self.client.get(reverse('home:cart_detail'))

        self.assertEqual(response.status_code, 200)

    def test_cart_detail_does_not_have_a_session(self):
        response = self.client.get(reverse('home:cart_detail'))

        self.assertEqual(response.status_code, 200)
