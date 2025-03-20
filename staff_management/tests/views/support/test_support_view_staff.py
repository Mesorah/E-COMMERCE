from django.test import TestCase
from django.urls import resolve, reverse

from staff_management import views
from utils.for_tests.base_for_authentication import register_super_user


class TestSupportViewStaff(TestCase):
    def setUp(self):
        register_super_user()

        self.client.login(username='test', password='123')

        return super().setUp()

    def test_if_staff_support_view_staff_load_the_correct_view(self):
        response = resolve(reverse('staff:support_view_staff'))

        self.assertEqual(response.func.view_class, views.SupportViewStaff)

    def test_if_staff_support_view_staff_load_the_correct_template(self):
        response = self.client.get(reverse('staff:support_view_staff'))

        self.assertTemplateUsed(
            response,
            'staff_management/pages/support_view_staff.html'
        )

    def test_if_staff_support_view_staff_returns_200(self):
        response = self.client.get(reverse('staff:support_view_staff'))

        self.assertEqual(response.status_code, 200)
