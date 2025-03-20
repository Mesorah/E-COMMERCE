from django.test import TestCase
from django.urls import resolve, reverse

from staff_management import views
from utils.for_tests.base_for_authentication import (  # noqa E501
    register_super_user,
    register_user,
)
from utils.for_tests.base_for_create_itens import create_product

# from django.utils.http import urlencode


class TestDeleteProductView(TestCase):
    def setUp(self):
        super_user = register_super_user()
        self.client.login(username='test', password='123')

        self.product = create_product(super_user)

        register_user()

        return super().setUp()

    def test_if_staff_delete_product_load_the_correct_view(self):
        response = resolve(reverse('staff:delete_product', kwargs={'pk': '1'}))

        self.assertEqual(response.func.view_class, views.ProductDeleteView)

    def test_user_without_permission_redirects_from_staff_delete_product(self):
        self.client.login(username='Test', password='Test')

        response = self.client.get(
            reverse(
                'staff:delete_product', kwargs={'pk': '1'}
            ), follow=True
        )

        # expected_url = reverse('authors:login') + '?' + urlencode(
        #     {'next': reverse(
        #         'staff:delete_product', kwargs={'pk': '1'}
        #         )
        #      }
        #  )

        self.assertRedirects(response, reverse('home:index'))

    def test_user_attempts_delete_product_with_get(self):
        response = self.client.get(
            reverse(
                'staff:delete_product', kwargs={'pk': '1'}
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_user_can_delete_product_in_staff(self):
        response = self.client.post(
            reverse(
                'staff:delete_product', kwargs={'pk': '1'}
            )
        )

        self.assertEqual(response.status_code, 302)

    """ Depois se tiver a página de confirmação """
    # def test_if_delete_product_have_the_correct_template(self):
    #     response = self.client.get(
    #         reverse(
    #             'staff:delete_product', kwargs={'id': '1'}
    #         )
    #     )

    #     self.assertTemplateUsed(
    #         response,
    #         'staff_management/pages/crud_item.html'
    #     )

    def test_delete_product_raises_404_if_not_found(self):
        response = self.client.post(
            reverse(
                'staff:delete_product', kwargs={'pk': '2'}
            )
        )

        self.assertEqual(response.status_code, 404)
