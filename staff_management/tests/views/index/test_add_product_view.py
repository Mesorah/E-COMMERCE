from django.test import TestCase
from django.urls import resolve, reverse
from django.utils.http import urlencode

from home.models import Products
from staff_management import views
from staff_management.forms import CrudProduct
from utils.for_tests.base_for_authentication import (  # noqa E501
    register_super_user,
    register_user,
)


class TestAddProductView(TestCase):
    def setUp(self):
        register_super_user()

        self.data = {
            'name': 'TEST PRODUCT',
            'price': '100',
            'description': 'THIS IS A TEST PRODUCT',
            'stock': '1',
            'is_published': True
        }

        return super().setUp()

    def test_if_staff_add_product_load_the_correct_view(self):
        response = resolve(reverse('staff:add_product'))

        self.assertEqual(response.func.view_class, views.ProductCreateView)

    def test_user_without_permission_redirects_from_staff_add_product(self):
        register_user()

        self.client.login(username='Test', password='Test')

        response = self.client.get(reverse('staff:add_product'), follow=True)

        expected_url = reverse('authors:login') + '?' + urlencode(
            {'next': reverse(
                'staff:add_product'
                )
             }
         )

        """
            Exemplo do urlencode:
                params = {
                    'next': '/staff_management/add_product/',
                    'search': 'Django test'
                }
                query_string = urlencode(params)

                print(query_string)
                # Saída: 'next=%2Fstaff_management%2Fadd_product%2F&search=
                # Django+test'
        """

        self.assertRedirects(response, expected_url)

    def test_user_with_permissions_can_add_product_in_staff_and_gets_200(self):
        self.client.login(username='test', password='123')

        response = self.client.get(reverse('staff:add_product'))

        self.assertEqual(response.status_code, 200)

    def test_if_add_product_have_the_correct_template(self):
        self.client.login(username='test', password='123')

        response = self.client.get(reverse('staff:add_product'))

        self.assertTemplateUsed(
            response,
            'staff_management/pages/crud_item.html'
        )

    def test_staff_add_product_post_redirects_with_302(self):
        self.client.login(username='test', password='123')

        response = self.client.post(
            reverse('staff:add_product'),
            data=self.data
        )

        self.assertEqual(response.status_code, 302)

    def test_item_count_increases_when_product_is_added(self):
        self.client.login(username='test', password='123')

        count = Products.objects.count()
        self.assertEqual(count, 0)

        self.client.post(
            reverse('staff:add_product'),
            data=self.data
        )

        new_count = Products.objects.count()

        self.assertEqual(new_count, 1)

    def test_add_product_form_is_invalid_when_data_is_incomplete(self):
        self.client.login(username='test', password='123')

        data = {
            'name': 'a',
            'price': '-5',
            'description': '',
            'stock': '-1'
        }

        response = self.client.post(
            reverse('staff:add_product'),
            data=data
        )

        form = CrudProduct(data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('price', form.errors)
        self.assertIn('stock', form.errors)
        self.assertIn('Nome de produto muito pequeno,', form.errors['name'][0])
        self.assertIn('Certifique-se que este valor seja maior ou igual a 0.',
                      form.errors['price'][0]
                      )
        self.assertIn('Certifique-se que este valor seja maior ou igual a 0.',
                      form.errors['stock'][0]
                      )
