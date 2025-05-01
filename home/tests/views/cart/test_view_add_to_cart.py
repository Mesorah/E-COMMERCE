from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import resolve, reverse

from home import views
from utils.for_tests.base_for_authentication import register_super_user
from utils.for_tests.base_for_create_itens import create_product


class TestViewAddToCart(TestCase):
    def setUp(self):
        user = register_super_user()
        self.client.login(username='test', password='123')

        self.product1 = create_product(user, stock=2)
        self.product2 = create_product(user, name='teste product 2')

        return super().setUp()

    def test_home_add_to_cart_load_the_correct_view(self):
        response = resolve(reverse('home:add_to_cart', kwargs={'pk': '1'}))

        self.assertEqual(response.func.view_class, views.AddToCartView)

    def test_home_add_to_cart_is_get(self):
        response = self.client.get(reverse(
            'home:add_to_cart',
            kwargs={'pk': '2'}
        ))

        self.assertEqual(response.status_code, 405)  # Navegador recusa

    def test_home_add_to_cart_is_post(self):
        response = self.client.post(reverse(
            'home:add_to_cart',
            kwargs={'pk': '1'}),
            data={'quantity': '1'},
            follow=True
        )

        self.assertEqual(len(self.client.session['cart']), 1)

        self.assertRedirects(response, reverse('home:index'))

    def test_add_to_cart_stock_is_not_enough(self):
        response = self.client.post(reverse(
            'home:add_to_cart',
            kwargs={'pk': '2'}),
            data={'quantity': '10'},
            follow=True
        )

        self.assertRedirects(response, reverse(
            'home:view_page',
            kwargs={'slug': self.product2.slug}
            )
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            'Não temos essa quantidade em estoque!'
        )

    def test_add_to_cart_using_sessions(self):
        response = self.client.post(
            reverse('home:add_to_cart', kwargs={'pk': '1'})
        )

        self.assertEqual(response.status_code, 302)

        response2 = self.client.post(
            reverse('home:add_to_cart', kwargs={'pk': '2'})
        )

        self.assertEqual(response2.status_code, 302)

    def test_add_to_cart_quantity_is_correct(self):
        self.client.post(
            reverse('home:add_to_cart', kwargs={'pk': '1'})
        )

        self.client.post(
            reverse('home:add_to_cart', kwargs={'pk': '1'})
        )

        self.client.post(
            reverse('home:add_to_cart', kwargs={'pk': '2'})
        )

        session = self.client.session['cart']

        quantities = [data['quantity'] for data in session.values()]

        self.assertEqual(quantities[0], 2)
        self.assertEqual(quantities[1], 1)
