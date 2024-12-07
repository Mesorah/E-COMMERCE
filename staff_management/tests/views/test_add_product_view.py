from django.test import TestCase
from utils.for_tests.base_for_authentication import (
    register_user,
    register_super_user
)
from django.urls import reverse
from home.models import Products
from staff_management.forms import CrudProduct


class TestHomeView(TestCase):
    def setUp(self):
        register_super_user()

        self.data = {
            'name': 'TEST PRODUCT',
            'price': '100',
            'description': 'THIS IS A TEST PRODUCT'
        }

        return super().setUp()

    def test_user_without_permission_redirects_from_staff_add_product(self):
        register_user()

        self.client.login(username='Test', password='Test')

        response = self.client.get(reverse('staff:add_product'))

        self.assertEqual(response.status_code, 302)

    def test_user_with_permissions_can_add_product_in_staff_and_gets_200(self):
        self.client.login(username='test', password='123')

        response = self.client.get(reverse('staff:add_product'))

        self.assertEqual(response.status_code, 200)

    def test_if_add_product_hava_the_correct_template(self):
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
            'description': ''
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
        self.assertIn('Nome de produto muito pequeno,', form.errors['name'][0])
        self.assertIn('o valor do produto não pode ser menor ou igual a 0',
                      form.errors['price'][0]
                      )
